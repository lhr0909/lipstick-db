import React from "react";
import type { ReactElement } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import Image from "next/image";
import { Typography, List, Descriptions, Tag, Card } from "antd";
import useSWR from "swr";

import { url, fetcher } from "utils/request";
import { Lipstick, LIPSTICK_TAG_COLORS } from "utils/model";
import { AppLayout } from "components/AppLayout";
import { LipstickTrialImage } from "components/LipstickTrialImage";

const { Title, Paragraph } = Typography;

export default function LipstickPage(props: { body: string }) {
  const router = useRouter();
  const { id } = router.query;
  const { data, error } = useSWR(() => !id ? null : url(`/lipsticks/${id}`), fetcher);
  return (
    <>
      <Title level={2}>口红详细信息</Title>
      <List
        itemLayout="vertical"
        size="large"
        dataSource={data ? [data] : []}
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
            <Title level={5}>试色图</Title>
            <List
              grid={{
                gutter: 8,
                xs: 1,
              }}
              dataSource={item.trial_images}
              renderItem={(trial: { uri: string; id: string }) => (
                <List.Item>
                  <LipstickTrialImage
                    lipstickId={item.id}
                    trialImageId={trial.id}
                    trialImageUri={trial.uri}
                  />
                </List.Item>
              )}
            />
          </List.Item>
        )}
      />
    </>
  );
}

LipstickPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout>
      <Head>
        <title>Lipstick Detail - Lipstick DB</title>
      </Head>
      {page}
    </AppLayout>
  );
};
