import React, { FC } from 'react';
import useSWR from 'swr';
import { Card } from 'antd';

import { Lipstick } from 'utils/model';
import { fetcher, url } from 'utils/request';

interface LipstickSearchResultProps {
  lipstickId: string;
  trialImageId: string;
  score: number
}

export const LipstickSearchResult: FC<LipstickSearchResultProps> = ({
  lipstickId,
  trialImageId,
  score,
}) => {
  const { data: lipstick, error } = useSWR<Lipstick>(
    url('/lipsticks/' + lipstickId),
    fetcher,
  );

  return !lipstick ? null : (
    <Card
      hoverable
      style={{ width: 200 }}
      cover={
lipstick.trial_images.find(trialImage => trialImage.id === trialImageId) && (
          <img src={(lipstick.trial_images.find(trialImage => trialImage.id === trialImageId) as any).uri} />
        )
      }
    >
      {/* <img src={lipstick.product_image} /> */}
      <Card.Meta
        title={lipstick.brand + ' ' + lipstick.nickname}
        description={`相似度：${Math.floor((1 - score) * 10000) / 100}%`}
      />
    </Card>
  );
};
