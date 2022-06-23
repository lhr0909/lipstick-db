import React, { useState } from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import { Typography, Row, Col, Button, Switch, Space, List } from "antd";
import type { UploadFile } from "antd/es/upload/interface";

import { url, fetcher } from "utils/request";
import { SearchMatch, SearchResult } from "utils/model";
import { AppLayout } from "components/AppLayout";
import { S3UploadControl } from "components/S3UploadControl";
import { LipstickSearchResult } from "components/LipstickSearchResult";
import { Palette } from 'components/Palette';
import { SearchOutlined } from "@ant-design/icons";

const { Title, Paragraph } = Typography;

export default function PlaygroundPage(props: { body: string }) {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [isLipSearch, setLipSearch] = useState<boolean>(false);
  const [searching, setSearching] = useState<boolean>(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  async function triggerSearch(): Promise<void> {
    setSearching(true);
    const embeddings = await Promise.all(fileList.map(async (file) => {
      const response = await fetcher(url(`/index/${file.uid}.${file.name.split(".").pop()}`));
      file.response = response;
      return response[isLipSearch ? 1 : 0].embedding;
    }));
    const results = await fetcher(url('/search'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        embeddings,
        search_type: isLipSearch ? 'lip' : 'skin',
      }),
    });
    setSearching(false);
    setSearchResults(results);
  }

  return (
    <>
      <Title level={2}>口红搜索</Title>
      <Paragraph>上传自拍，让AI给你找合适的口红！</Paragraph>
      <Row justify="center">
        <Col span={24}>
          <S3UploadControl fileList={fileList} setFileList={setFileList} searching={searching} />
        </Col>
      </Row>
      <Row>
        <Col span={24}>
          <Space className="my-2">
            <Switch
              checkedChildren="唇色搜索"
              unCheckedChildren="肤色搜索"
              checked={isLipSearch}
              onChange={setLipSearch}
              loading={searching}
            />
            <Button
              type="primary"
              icon={<SearchOutlined />}
              onClick={triggerSearch}
              loading={searching}
            >搜索</Button>
          </Space>
        </Col>
      </Row>
      {searchResults && searchResults.length > 0 && (
        <Row className="mt-8">
          <Col span={24}>
            <Title level={3}>搜索结果</Title>
            <List
              itemLayout="vertical"
              size="large"
              dataSource={fileList.map((file: UploadFile, idx: number) => {
                const result: SearchResult = searchResults[idx];
                return [file, result] as [UploadFile, SearchResult];
              })}
              renderItem={([file, result]: [UploadFile, SearchResult]) => (
                <List.Item
                  key={file?.uid}
                >
                  {(!file || !result) ? null : (
                    <List
                      header={
                        <Row>
                          <Col xs={24} md={12}>
                            <img className="block mx-auto" style={{ maxWidth: 200 }} src={file.url || file.thumbUrl} alt={file.name} />
                          </Col>
                          <Col xs={24} md={12}>
                            {!file.response ? null : (
                              <div className="my-4" style={{ minWidth: 200 }}>
                                {isLipSearch ? null : (
                                  <>
                                    <Typography.Paragraph>脸部颜色</Typography.Paragraph>
                                    <Palette colors={file.response[0].tensor}></Palette>
                                  </>
                                )}
                                {!isLipSearch ? null : (
                                  <>
                                    <Typography.Paragraph>唇部颜色</Typography.Paragraph>
                                    <Palette colors={file.response[1].tensor}></Palette>
                                  </>
                                )}
                              </div>
                            )}
                          </Col>
                        </Row>
                      }
                      grid={{ gutter: 8, xs: 1, sm: 2, md: 3, lg: 4, column: 5 }}
                      dataSource={result.matches}
                      renderItem={(match: SearchMatch) => (
                        <LipstickSearchResult
                          isLipSearch={isLipSearch}
                          key={`${match.lipstick_id}-${match.trial_image_id}`}
                          lipstickId={match.lipstick_id}
                          trialImageId={match.trial_image_id}
                          score={match.score}
                        />
                      )}
                    />
                  )}
                </List.Item>
              )}
            />
          </Col>
        </Row>
      )}
    </>
  );
}

PlaygroundPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>口红搜索 - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
