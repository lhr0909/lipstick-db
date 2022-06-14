import React, { FC, ReactNode } from "react";
import { Layout } from "antd";
import { useRouter } from "next/router";
import Link from "next/link";

import { SideNav } from "./SideNav";

import styles from "styles/AppLayout.module.css";

const { Content, Footer } = Layout;

interface AppLayoutProps {
  children?: ReactNode;
}

export const AppLayout: FC<AppLayoutProps> = ({ children }: AppLayoutProps) => {
  const router = useRouter();

  return (
    <Layout
      className="min-h-screen"
    >
      <SideNav selected={router.pathname} />
      <Layout className="bg-white">
        <Content className="p-4 pb-20 pt-20">
          <div
            className={`${styles["content-container"]} h-full w-full bg-white`}
          >
            {children}
          </div>
        </Content>
        <Footer
          className="footer w-full h-20 flex text-center items-center justify-center fixed bottom-0"
        >
          {`Made with <3 by`}
          &nbsp;
          <Link href="https://divby0.io">Simon Liang</Link>
          &nbsp;
          {`in 2022`}
        </Footer>
      </Layout>
    </Layout>
  );
};
