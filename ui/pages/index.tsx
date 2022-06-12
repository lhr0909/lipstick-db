import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import { Typography } from "antd";

import { AppLayout } from "components/AppLayout";

const { Title, Paragraph } = Typography;

export default function IndexPage(props: { body: string }) {
  return (
    <>
      <Title level={2}>Lipstick DB</Title>
      <Paragraph>找到最适合你的口红！</Paragraph>
    </>
  );
}

IndexPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
