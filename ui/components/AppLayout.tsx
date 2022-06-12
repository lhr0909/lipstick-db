import React, { FC, ReactNode } from "react";
import { Layout } from "antd";
import { useRouter } from "next/router";
import createPersistedState from "use-persisted-state";

import { SideNav } from "./SideNav";

import styles from "styles/AppLayout.module.css";

const { Content, Footer } = Layout;

const useCollapsedState = createPersistedState("side-nav-collapsed");

interface AppLayoutProps {
  children?: ReactNode;
}

export const AppLayout: FC<AppLayoutProps> = ({ children }: AppLayoutProps) => {
  const router = useRouter();
  const [collapsed, setCollapsed] = useCollapsedState(false);

  return (
    <Layout
      className="min-h-screen"
      style={{ marginLeft: collapsed ? "80px" : "200px" }}
    >
      <SideNav
        selected={router.pathname}
        collapsed={collapsed as boolean}
        setCollapsed={setCollapsed}
      />
      <Layout className="bg-white">
        <Content className="p-4 pb-20">
          <div
            className={`${styles["content-container"]} h-full w-full bg-white`}
          >
            {children}
          </div>
        </Content>
        <Footer
          className="footer w-full h-20 flex text-center items-center justify-center fixed bottom-0"
          style={{ paddingRight: collapsed ? "80px" : "200px" }}
        >
          Made with &lt;3 by Simon Liang in 2022
        </Footer>
      </Layout>
    </Layout>
  );
};
