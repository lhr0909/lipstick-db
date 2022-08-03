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
      <Paragraph>Find the right lipstick using AI!</Paragraph>
      <Paragraph>
        <img
          src="https://jina.ai/assets/images/logo.svg"
          alt="jina"
          style={{
            height: 80,
          }}
        />
      </Paragraph>
      <Paragraph>Powered by Jina</Paragraph>
      <Paragraph>
        Jina is a framework that empowers anyone to build cross-modal and
        multi-modal. Visit their{" "}
        <a
          href="https://github.com/jina-ai/jina"
          target="_blank"
          rel="noreferrer"
        >
          repo
        </a>{" "}
        and give a star!
      </Paragraph>
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
