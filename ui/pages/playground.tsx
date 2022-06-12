import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import { Typography } from "antd";

import { AppLayout } from "components/AppLayout";

const { Title, Paragraph } = Typography;

export default function PlaygroundPage(props: { body: string }) {
  return (
    <>
      <Title level={2}>Playground</Title>
      <Paragraph>Playground Page</Paragraph>
    </>
  );
}

PlaygroundPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>Playground - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
