import { AvatarDropdown, AvatarName, Footer, Question, SelectLang } from '@/components';
import { useDomainName } from '@/hooks';
import { listDomainsBrickapiV1DomainsGet } from '@/services/brick-server-playground/domains';
import { usersCurrentUserBrickapiV1UsersMeGet as queryCurrentUser } from '@/services/brick-server-playground/users';
import {CodeOutlined, LinkOutlined, SmileOutlined, BuildOutlined, ThunderboltOutlined } from '@ant-design/icons';
import type { Settings as LayoutSettings, MenuDataItem } from '@ant-design/pro-components';
import { SettingDrawer } from '@ant-design/pro-components';
import type { RunTimeLayoutConfig } from '@umijs/max';
import { Link, history, useAccess } from '@umijs/max';
import { Flex, Select, SelectProps, Typography } from 'antd';
import { map, trimEnd } from 'lodash';
import { useState } from 'react';
import defaultSettings from '../config/defaultSettings';
import { errorConfig } from './requestErrorConfig';

import hljsDefineSparql from '@/utils/sparql';
import hljsDefineTurtle from '@/utils/turtle';
import hljs from 'highlight.js/lib/core';
import 'highlight.js/styles/github.css';

hljsDefineTurtle(hljs);
hljsDefineSparql(hljs);

import json from 'highlight.js/lib/languages/json';
import plaintext from 'highlight.js/lib/languages/plaintext';

hljs.registerLanguage('json', json);
hljs.registerLanguage('plaintext', plaintext);

const isDev = process.env.NODE_ENV === 'development';
const loginPath = '/user/login';

/**
 * @see  https://umijs.org/zh-CN/plugins/plugin-initial-state
 * */
export async function getInitialState(): Promise<{
  settings?: Partial<LayoutSettings>;
  currentUser?: API.UserRead;
  loading?: boolean;
  fetchUserInfo?: () => Promise<API.UserRead | undefined>;
  currentDomain?: API.DomainRead | null;
  currentDomainUser?: API.DomainUserRead | null;
  // setCurrentDomain?: () => void,
}> {
  const fetchUserInfo = async () => {
    try {
      const msg = await queryCurrentUser();
      console.log(msg);
      if (msg.errorCode !== 'Success') {
        throw Error(msg.errorCode);
      }
      return msg.data as API.UserRead;
    } catch (error) {
      history.push(loginPath);
    }
    return undefined;
  };

  /*
    const defaultCurrentDomain = (): API.DomainRead | undefined => {
      const data = localStorage.getItem('CURRENT_CONTEST');
      if (!data) return undefined;
      try {
        const currentDomain: API.DomainRead = JSON.parse(data);
        if (currentDomain && currentDomain.id && currentDomain.name) {
          return currentDomain;
        }
        // eslint-disable-next-line no-empty
      } catch {}
      return undefined;
    };

    const setCurrentDomain = (currentDomain?: API.DomainRead) => {
      localStorage.setItem('CURRENT_CONTEST', JSON.stringify(currentDomain));
    };
  */

  // 如果不是登录页面，执行
  const { location } = history;
  const trimmedPath = trimEnd(location.pathname, '/');
  if (location.pathname !== trimmedPath) {
    history.push(trimmedPath + location.search);
  }
  if (trimmedPath !== loginPath) {
    const currentUser = await fetchUserInfo();
    return {
      fetchUserInfo,
      currentUser,
      settings: defaultSettings as Partial<LayoutSettings>,
    };
  }
  return {
    fetchUserInfo,
    settings: defaultSettings as Partial<LayoutSettings>,
  };
}

// ProLayout 支持的api https://procomponents.ant.design/components/layout
const Layout: RunTimeLayoutConfig = ({ initialState, setInitialState }) => {
  const [domains, setDomains] = useState<API.DomainRead[]>([]);
  const domainName = useDomainName();
  const access = useAccess();

  const domainOptions = map(domains, (domain: API.DomainRead) => ({
    value: domain.name,
    label: domain.name,
    domain: domain,
  }));
  const onFocusDomainSelect: SelectProps['onFocus'] = async () => {
    if (domains.length > 0) return;
    const result: API.DomainReadListResp = await listDomainsBrickapiV1DomainsGet();
    if (result.data?.results) {
      setDomains(result.data?.results);
    }
  };

  const onSelectDomainSelect: SelectProps['onSelect'] = async (label, option) => {
    await setInitialState({ ...initialState, currentDomain: option.domain });
    history.push(`/domain/${option.value}/dashboard`);
  };

  return {
    menu: {
      params: {
        userId: initialState?.currentDomain?.name,
      },
      request: async (params: any, defaultMenuData: any) => {
        const menu: MenuDataItem[] = [
          {
            path: '/welcome',
            name: 'welcome',
            icon: <SmileOutlined />,
          },
        ];
        const domainName = initialState?.currentDomain?.name;
        if (domainName) {
          let children = [
            {
              path: `/domain/${domainName}/dashboard`,
              name: 'dashboard',
            },
            {
              path: `/domain/${domainName}/appstore`,
              name: 'appstore',
            },
            {
              path: `/domain/${domainName}/app/:appName`,
              hideInMenu: true,
            },
          ];
          if (access.isDomainAdmin) {
            children = children.concat([
              {
                path: `/domain/${domainName}/settings`,
                name: 'settings',
              },
              {
                path: `/domain/${domainName}/users`,
                name: 'users',
              },
              {
                path: `/domain/${domainName}/apps`,
                name: 'apps',
              },
              {
                path: `/domain/${domainName}/resources`,
                name: 'resources',
              },
              {
                path: `/domain/${domainName}/policies`,
                name: 'policies',
              },
              {
                path: `/domain/${domainName}/profiles`,
                name: 'profiles',
              },
            ]);
          }
          menu.push({
            path: `/domain/${domainName}`,
            name: 'domain',
            children: children,
            icon: <BuildOutlined />,
          });
        }
        menu.push({
          name: 'developer',
          children: [
            {
              path: '/developer/apps',
              name: 'apps'
            }
          ],
          icon: <CodeOutlined />,
        });
        if (access.isSiteAdmin) {
          menu.push({
            name: 'admin',
            children: [
              {
                path: '/admin/apps',
                name: 'apps'
              },
              {
                path: '/admin/domains',
                name: 'domains'
              }
            ],
            icon: <ThunderboltOutlined/>,
          });
        }
        return menu;
      },
    },
    onMenuHeaderClick: () => {},
    headerTitleRender: () => {
      return (
        <Flex align="center" gap="large">
          <Typography.Title>Brick Server Playground</Typography.Title>
          <Select
            placeholder="Select domain"
            options={domainOptions}
            onFocus={onFocusDomainSelect}
            onSelect={onSelectDomainSelect}
            defaultValue={domainName || undefined}
          ></Select>
        </Flex>
      );
    },
    // actionsRender: () => [<Question key="doc" />, <SelectLang key="SelectLang" />],
    avatarProps: {
      // src: initialState?.currentUser?.avatar,
      title: <AvatarName />,
      render: (_, avatarChildren) => {
        return <AvatarDropdown>{avatarChildren}</AvatarDropdown>;
      },
    },
    // waterMarkProps: {
    //   content: initialState?.currentUser?.name,
    // },
    footerRender: () => <Footer />,
    style: {
      minHeight: '100vh',
    },
    onPageChange: () => {
      const { location } = history;
      // 如果没有登录，重定向到 login
      if (!initialState?.currentUser && location.pathname !== loginPath) {
        history.push(loginPath);
      }
    },
    bgLayoutImgList: [
      {
        src: 'https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/D2LWSqNny4sAAAAAAAAAAAAAFl94AQBr',
        left: 85,
        bottom: 100,
        height: '303px',
      },
      {
        src: 'https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/C2TWRpJpiC0AAAAAAAAAAAAAFl94AQBr',
        bottom: -68,
        right: -45,
        height: '303px',
      },
      {
        src: 'https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/F6vSTbj8KpYAAAAAAAAAAAAAFl94AQBr',
        bottom: 0,
        left: 0,
        width: '331px',
      },
    ],
    links: isDev
      ? [
          <Link key="openapi" to="/umi/plugin/openapi" target="_blank">
            <LinkOutlined />
            <span>OpenAPI 文档</span>
          </Link>,
        ]
      : [],
    menuHeaderRender: undefined,
    locale: "en-US",
    // 自定义 403 页面
    // unAccessible: <div>unAccessible</div>,
    // 增加一个 loading 的状态
    childrenRender: (children) => {
      // if (initialState?.loading) return <PageLoading />;
      return (
        <>
          {children}
          {isDev && (
            <SettingDrawer
              disableUrlParams
              enableDarkTheme
              settings={initialState?.settings}
              onSettingChange={(settings) => {
                setInitialState((preInitialState) => ({
                  ...preInitialState,
                  settings,
                }));
              }}
            />
          )}
        </>
      );
    },
    ...initialState?.settings,
  };
};

export const layout = Layout;

/**
 * @name request 配置，可以配置错误处理
 * 它基于 axios 和 ahooks 的 useRequest 提供了一套统一的网络请求和错误处理方案。
 * @doc https://umijs.org/docs/max/request#配置
 */
export const request = {
  ...errorConfig,
};
