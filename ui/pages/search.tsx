import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import { Typography } from "antd";

import { AppLayout } from "components/AppLayout";

const { Title, Paragraph } = Typography;

export default function PlaygroundPage(props: { body: string }) {
  return (
    <>
      <Title level={2}>Search Lipstick with your Selfie!</Title>
      <Paragraph>找到适合你的口红！</Paragraph>
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
