import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import Image from "next/image";
import { Typography, List, Descriptions, Tag } from "antd";
import useSWR from "swr";

import { url, fetcher } from "utils/request";
import { Lipstick, LIPSTICK_TAG_COLORS } from "utils/model";
import { AppLayout } from "components/AppLayout";

const { Title, Paragraph } = Typography;

export default function LipsticksPage(props: { body: string }) {
  const { data, error } = useSWR(url("/lipsticks"), fetcher);
  return (
    <>
      <Title level={2}>Lipsticks</Title>
      <Paragraph>The collection of all of our lipsticks.</Paragraph>
      <List
        itemLayout="vertical"
        size="large"
        dataSource={data}
        renderItem={(item: Lipstick) => (
          <List.Item
            extra={
              <Image
                src={item.product_image}
                alt={item.nickname}
                height={300}
                width={300}
              />
            }
          >
            <Descriptions layout="vertical" title={`${item.brand} ${item.nickname}`}>
              <Descriptions.Item label="品牌">{item.brand}</Descriptions.Item>
              <Descriptions.Item label="色号">{item.color}</Descriptions.Item>
              <Descriptions.Item label="关键字">
                {(item.meta.type || []).map((keyword: string) => (
                  <Tag key={keyword} color={LIPSTICK_TAG_COLORS[keyword]}>
                    {keyword}
                  </Tag>
                ))}
              </Descriptions.Item>
            </Descriptions>
          </List.Item>
        )}
      />
    </>
  );
}

LipsticksPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>All Lipsticks - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
