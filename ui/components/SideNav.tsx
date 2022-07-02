import React, { FC } from "react";
import Link from "next/link";
import { Layout, Menu } from "antd";
import Icon, { HomeOutlined, SearchOutlined } from "@ant-design/icons";

import LipstickIcon from './LipstickIcon';

const { Header } = Layout;

interface SideNavProps {
  selected: string;
}

export const SideNav: FC<SideNavProps> = ({
  selected,
}: SideNavProps) => (
  <Header className="bg-white header w-full z-50 h-20 flex text-center items-center justify-center fixed top-0">
    <Menu mode="horizontal" defaultSelectedKeys={[selected]}>
      <Menu.Item key="/" icon={<HomeOutlined />}>
        <Link href="/">首页</Link>
      </Menu.Item>
      {/* <Menu.Item key="/lipsticks" icon={<Icon component={LipstickIcon} />}>
        <Link href="/lipsticks">口红</Link>
      </Menu.Item> */}
      <Menu.Item key="/search" icon={<SearchOutlined />}>
        <Link href="/search">搜索</Link>
      </Menu.Item>
    </Menu>
  </Header>
);
