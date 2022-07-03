import React, { FC } from "react";
import { useRouter } from "next/router";
import { Layout, Menu } from "antd";
import Icon, { GlobalOutlined, HomeOutlined, SearchOutlined } from "@ant-design/icons";

import LipstickIcon from './LipstickIcon';

const { Header } = Layout;

interface SideNavProps {
  selected: string;
}

export const SideNav: FC<SideNavProps> = ({
  selected,
}: SideNavProps) => {
  const router = useRouter();
  const isEnglish = selected.startsWith('/en');
  const items = [
    {
      label: isEnglish ? 'Home' : '首页',
      key: isEnglish ? '/en' : '/',
      icon: <HomeOutlined />,
      onClick: () => router.push(isEnglish ? '/en' : '/'),
    },
    {
      label: isEnglish ? 'Search' : '搜索',
      key: isEnglish ? '/en/search' : '/search',
      icon: <SearchOutlined />,
      onClick: () => router.push(isEnglish ? '/en/search' : '/search'),
    },
    {
      label: isEnglish ? '中文' : 'English',
      key: isEnglish ? '/' : '/en',
      icon: <GlobalOutlined />,
      onClick: () => router.push(isEnglish ? '/' : '/en'),
    },
  ];

  return (
    <Header className="bg-white header w-full z-50 h-20 flex items-center justify-center fixed top-0">
      <Menu style={{ minWidth: 300 }} mode="horizontal" defaultSelectedKeys={[selected]} items={items} />
    </Header>
  );
};
