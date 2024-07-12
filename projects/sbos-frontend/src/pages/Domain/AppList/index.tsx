import { useDomainName } from '@/hooks';
import { appsListBrickapiV1AppsGet } from '@/services/brick-server-playground/apps';
import {
  domainApproveAppBrickapiV1DomainsDomainAppsAppPost,
  domainListAppBrickapiV1DomainsDomainAppsGet,
} from '@/services/brick-server-playground/domains';
import { useRequest } from '@@/exports';
import { PageContainer } from '@ant-design/pro-components';
import { Button, Card, Col, Row, Typography } from 'antd';
import React from 'react';

const AppList: React.FC = () => {
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
  const { data: apps, refresh: reloadApps } = useRequest(
    async () => {
      return await appsListBrickapiV1AppsGet();
    },
    {
      // manual: true,
      onSuccess: (data: API.AppReadResp) => {
        console.log(data);
      },
    },
  );
  const approvedAppsId = new Set();
  for (let i = 0; i < domainApps?.results.length; i++) {
    approvedAppsId.add(domainApps.results[i].app.id);
  }
  console.log(approvedAppsId);

  const AppCard = (app: API.AppRead) => {
    const handleApproveApp = async () => {
      const result = await domainApproveAppBrickapiV1DomainsDomainAppsAppPost({
        domain: domainName,
        app: app.id,
      });
      console.log(result);
      reloadDomainApps();
    };

    return (
      <Col xxl={6} xl={8} lg={8} md={8} sm={12} xs={24} key={app.id}>
        <Card title={app.name} bordered={false}>
          <Typography.Paragraph>{app.description}</Typography.Paragraph>
          {approvedAppsId.has(app.id) ? (
            <Button disabled>Approved</Button>
          ) : (
            <Button type="primary" onClick={handleApproveApp}>
              Approve
            </Button>
          )}
        </Card>
      </Col>
    );
  };

  return (
    <PageContainer>
      <Row gutter={16}>{apps?.results.map((app: API.AppRead) => AppCard(app))}</Row>
    </PageContainer>
  );
};

export default AppList;
