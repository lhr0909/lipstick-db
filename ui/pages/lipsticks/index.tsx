import React from "react";
import type { ReactElement } from "react";
import Head from "next/head";
import Image from "next/image";
import Link from "next/link";
import { Typography, List, Descriptions, Tag, Space } from "antd";
import useSWR from "swr";

import { url, fetcher } from "utils/request";
import { Lipstick, LIPSTICK_TAG_COLORS } from "utils/model";
import { AppLayout } from "components/AppLayout";

const { Title, Paragraph } = Typography;

export default function LipsticksPage(props: { body: string }) {
  const { data, error } = useSWR(url("/lipsticks"), fetcher);
  return (
    <>
      <Title level={2}>口红数据</Title>
      <Paragraph>目前数据库中所有的口红。</Paragraph>
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
            actions={[
              <Space key="trials">
                <Link href={`/lipsticks/${item.id}`}>查看试色图</Link>
              </Space>
            ]
            }
          >
            <Descriptions layout="vertical" title={`${item.brand} ${item.series} ${item.name || item.nickname} (${item.color})`}>
              <Descriptions.Item label="昵称">
                {item.nickname}
              </Descriptions.Item>
              <Descriptions.Item label="价格">
                ¥{item.meta.price}
              </Descriptions.Item>
              <Descriptions.Item label="类型">
                {(item.meta.type || []).map((keyword: string) => (
                  <Tag key={keyword} color={LIPSTICK_TAG_COLORS[keyword]}>
                    {keyword}
                  </Tag>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="质地">
                {(item.meta.texture || []).map((keyword: string) => (
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
        <title>口红数据 - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
