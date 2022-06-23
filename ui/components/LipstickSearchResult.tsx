import React, { FC } from 'react';
import useSWR from 'swr';
import Link from 'next/link';
import { Card, Space } from 'antd';
import Icon from '@ant-design/icons';

import { Lipstick, LipstickTrialImageColors } from 'utils/model';
import { fetcher, url } from 'utils/request';
import LipstickIcon from './LipstickIcon';
import { Palette } from './Palette';

interface LipstickSearchResultProps {
  isLipSearch: boolean;
  lipstickId: string;
  trialImageId: string;
  score: number;
}

export const LipstickSearchResult: FC<LipstickSearchResultProps> = ({
  isLipSearch,
  lipstickId,
  trialImageId,
  score,
}) => {
  const { data: lipstick } = useSWR<Lipstick>(
    url('/lipsticks/' + lipstickId),
    fetcher,
  );

  const { data: trialImageColors } = useSWR<LipstickTrialImageColors[]>(
    url('/lipsticks/' + lipstickId + '/trial_images/' + trialImageId),
    fetcher,
  );

  return !lipstick ? null : (
    <Card
      className="my-2 mx-auto"
      hoverable
      style={{ width: 200 }}
      cover={
lipstick.trial_images.find(trialImage => trialImage.id === trialImageId) && (
          <img style={{width: '99%', marginTop: '1px', marginLeft: '1px'}} src={lipstick.product_image} />
          // <img src={(lipstick.trial_images.find(trialImage => trialImage.id === trialImageId) as any).uri} />
        )
      }
      actions={[
        <Link key="view-lipstick" href={`/lipsticks/${lipstickId}`}>
          <Space>
            <Icon style={{ width: 14 }} component={LipstickIcon} />
            查看
          </Space>
        </Link>
      ]}
    >
      {/* {trialImageColors && (
        <Palette colors={trialImageColors[isLipSearch ? 1 : 0].tensor}></Palette>
      )} */}
      <Card.Meta
        title={lipstick.brand + ' ' + lipstick.nickname}
        description={`匹配度：${Math.floor((1 - score) * 10000) / 100}%`}
      />
    </Card>
  );
};
