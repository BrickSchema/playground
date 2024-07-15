import { useDomainName } from '@/hooks';
import NoFoundPage from '@/pages/404';
import { usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet } from '@/services/brick-server-playground/users';
import { PageContainer } from '@ant-design/pro-components';
import React from 'react';
import { useParams, useRequest } from 'umi';

const UserAppStore: React.FC = () => {
  const domainName = useDomainName();

  const { appName } = useParams<{ appName: string }>();

  const {
    data: domainUserApp,
    refresh: reloadDomainUserApp,
  }: { data?: API.DomainUserAppRead; refresh: any } = useRequest(
    async () => {
      return await usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet({
        domain: domainName,
        app: appName || '',
      });
    },
    {
      // manual: true,
      onSuccess: (data: API.DomainAppReadResp) => {
        console.log(data);
      },
    },
  );

  if (!domainUserApp?.app?.name) {
    return <NoFoundPage />;
  }

  return (
    <PageContainer title={domainUserApp.app.name}>
      <iframe
        title={domainUserApp.app.name}
        src={`/brickapi/v1/apps/${domainUserApp.app.name}/static/index.html?token=${domainUserApp.token}`}
        style={{ height: '75vh', width: '100%' }}
      />
    </PageContainer>
  );
};
export default UserAppStore;
