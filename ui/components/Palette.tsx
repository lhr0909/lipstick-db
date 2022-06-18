import React, { FC } from "react";
import { Card } from "antd";

interface PaletteProps {
  colors: number[][];
}

export const Palette: FC<PaletteProps> = ({
  colors,
}: PaletteProps) => {
  return !colors ? null : (
    <div className="w-full">
      {colors.map((color, idx) => (
        <span
          key={`color-${idx}`}
          className="inline-block"
          style={{
          width: "5%",
          height: 30,
          backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
        }} />
      ))}
    </div>
  );
};
