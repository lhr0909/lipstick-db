import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import { Typography, Row, Col } from "antd";

import { AppLayout } from "components/AppLayout";
import { S3UploadControl } from "components/S3UploadControl";

const { Title, Paragraph } = Typography;

export default function PlaygroundPage(props: { body: string }) {
  return (
    <>
      <Title level={2}>口红搜索</Title>
      <Paragraph>上传自拍，让AI给你找合适的口红！</Paragraph>
      <Row>
        <Col span={24}>
          <S3UploadControl />
        </Col>
      </Row>
    </>
  );
}

PlaygroundPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>Search - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
