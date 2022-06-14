import React, { FC } from "react";
import { Card, Typography } from "antd";
import useSWR from "swr";

import { url, fetcher } from "utils/request";
import { Palette } from "./Palette";

interface LipstickTrialImageProps {
  lipstickId: string;
  trialImageId: string;
  trialImageUri: string;
}

export const LipstickTrialImage: FC<LipstickTrialImageProps> = ({
  lipstickId,
  trialImageId,
  trialImageUri,
}: LipstickTrialImageProps) => {
  const { data, error } = useSWR(
    url(`/lipsticks/${lipstickId}/trial_images/${trialImageId}`),
    fetcher
  );

  return (
    <Card
      style={{
        width: 200,
      }}
      hoverable
      cover={<img src={trialImageUri} />}
    >
      {data && (
        <>
          <Typography.Paragraph>脸部颜色</Typography.Paragraph>
          <Palette colors={data[0].tensor}></Palette>
          <Typography.Paragraph>唇部颜色</Typography.Paragraph>
          <Palette colors={data[1].tensor}></Palette>
        </>
      )}
    </Card>
  );
};
