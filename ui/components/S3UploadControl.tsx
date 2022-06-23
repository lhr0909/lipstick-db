import React, { FC, useState } from "react";
import useSWR from "swr";
import { Upload, Modal, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import type { UploadFile, UploadChangeParam } from "antd/es/upload/interface";
import type { UploadRequestOption } from "rc-upload/es/interface";

import { url, fetcher } from "utils/request";
import { S3UploadResponse } from "utils/model";
import { Palette } from './Palette';

interface S3UploadControlProps {
  fileList: UploadFile[];
  setFileList: (fileList: UploadFile[]) => void;
  searching: boolean;
}

export const S3UploadControl: FC<S3UploadControlProps> = ({ fileList, setFileList, searching }) => {
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewFile, setPreviewFile] = useState<UploadFile | null>(null);
  const { data } = useSWR(() =>
    previewFile
      ? url(`/index/${previewFile.uid}.${previewFile.name.split(".").pop()}`)
      : null,
    fetcher,
  );

  async function getUploadLink(file: UploadFile): Promise<any> {
    const data = await fetcher(url("/upload"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filename: `${file.uid}.${file.name.split(".").pop()}`,
      }),
    });

    return data;
  }

  async function handlePreview(file: UploadFile) {
    console.log("onPreview", file);
    const signedUrl = await fetcher(file.response);
    file.url = signedUrl;
    setPreviewFile(file);
    setPreviewVisible(true);
  }

  function handleUploadChange({ file, fileList }: UploadChangeParam): void {
    console.log("onChange", fileList);
    setFileList(fileList);
  }

  async function uploadRequest({
    file,
    action,
    onSuccess,
    onError,
  }: UploadRequestOption): Promise<void> {
    try {
      const {
        url: postUrl,
        fields,
        filename,
      } = action as unknown as S3UploadResponse;
      const body = new FormData();
      for (const [key, value] of Object.entries(fields)) {
        body.append(key, value);
      }
      body.append("file", new File([file], filename));
      await fetch(postUrl, {
        method: "POST",
        body,
      });
      if (onSuccess) {
        onSuccess(url("/upload/" + filename));
      }
    } catch (err) {
      if (onError) {
        onError(err as any);
      }
    }
  }

  return (
    <>
      <Upload
        className="my-2"
        listType="picture-card"
        fileList={fileList}
        action={getUploadLink}
        onPreview={handlePreview}
        onChange={handleUploadChange}
        customRequest={uploadRequest}
      >
        {fileList.length >= 5 || searching ? null : (
          <div>
            <PlusOutlined />
            <div style={{ marginTop: 8 }}>上传</div>
          </div>
        )}
      </Upload>
      <Modal
        visible={previewVisible}
        title={previewFile?.name}
        footer={null}
        onCancel={() => setPreviewVisible(false)}
      >
        <img
          style={{ width: "100%" }}
          src={previewFile?.url || previewFile?.thumbUrl}
        />
        {data && (
          <>
            <Typography.Paragraph>脸部颜色</Typography.Paragraph>
            <Palette colors={data[0].tensor}></Palette>
            <Typography.Paragraph>唇部颜色</Typography.Paragraph>
            <Palette colors={data[1].tensor}></Palette>
          </>
        )}
      </Modal>
    </>
  );
};
