import { useDomainName } from '@/hooks';
import { domainListAppBrickapiV1DomainsDomainAppsGet } from '@/services/brick-server-playground/domains';
import {
  usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPost,
  usersListAppsBrickapiV1UsersDomainsDomainAppsGet,
  usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDelete,
} from '@/services/brick-server-playground/users';
import { PageContainer } from '@ant-design/pro-components';
import { Button, Card, Col, Row, Typography } from 'antd';
import React from 'react';
import { useRequest } from 'umi';

const UserAppStore: React.FC = () => {
  const domainName = useDomainName();

  const { data: domainApps, refresh: reloadDomainApps } = useRequest(
    async () => {
      return await domainListAppBrickapiV1DomainsDomainAppsGet({ domain: domainName || '' });
    },
    {
      // manual: true,
      onSuccess: (data: API.DomainAppReadResp) => {
        console.log(data);
      },
    },
  );
  const { data: domainUserApps, refresh: reloadDomainUserApps } = useRequest(
    async () => {
      return await usersListAppsBrickapiV1UsersDomainsDomainAppsGet({ domain: domainName || '' });
    },
    {
      // manual: true,
      onSuccess: (data: API.DomainAppReadResp) => {
        console.log(data);
      },
    },
  );

  const installedAppsId = new Set();
  for (let i = 0; i < domainUserApps?.results.length; i++) {
    installedAppsId.add(domainUserApps.results[i].app.id);
  }
  console.log(installedAppsId);

  const AppCard = (domainApp: API.DomainAppRead) => {
    const handleInstallApp = async () => {
      const result = await usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPost({
        domain: domainApp.domain.id,
        app: domainApp.app.id,
      });
      console.log(result);
      reloadDomainUserApps();
    };

    const handleUnInstallApp = async () => {
      const result = await usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDelete({
        domain: domainApp.domain.id,
        app: domainApp.app.id,
      });
      console.log(result);
      reloadDomainUserApps();
    };

    return (
      <Col xxl={6} xl={8} lg={8} md={8} sm={12} xs={24} key={domainApp.app.id}>
        <Card title={domainApp.app.name} bordered={false}>
          <Typography.Paragraph>{domainApp.app.description}</Typography.Paragraph>
          {installedAppsId.has(domainApp.app.id) ? (
            <Button danger onClick={handleUnInstallApp}>
              Uninstall
            </Button>
          ) : (
            <Button type="primary" onClick={handleInstallApp}>
              Install
            </Button>
          )}
        </Card>
      </Col>
    );
  };

  return (
    <PageContainer>
      <Row gutter={16}>
        {domainApps?.results.map((domainApp: API.DomainAppRead) => AppCard(domainApp))}
      </Row>
    </PageContainer>
  );
};
export default UserAppStore;
