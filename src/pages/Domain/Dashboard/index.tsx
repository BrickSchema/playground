import { useDomainName } from '@/hooks';
import { appsGetBrickapiV1AppsAppGet } from '@/services/brick-server-playground/apps';
import {
  usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet,
  usersListAppsBrickapiV1UsersDomainsDomainAppsGet,
  usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGet,
  usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGet,
  usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatch,
  usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPost,
  usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPost,
} from '@/services/brick-server-playground/users';
import {
  ExportOutlined,
  PauseCircleOutlined,
  PlayCircleOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import {
  ModalForm,
  PageContainer,
  ProCard,
  ProFormGroup,
  ProFormInstance,
  ProFormList,
  ProFormSelect,
  ProFormText,
} from '@ant-design/pro-components';
import { Col, Modal, Row, Spin, message } from 'antd';
import { findIndex, fromPairs, get, keys, map, union, values, zipObject } from 'lodash';
import React, { useRef, useState } from 'react';
import { useRequest } from 'umi';

const Dashboard: React.FC = () => {
  const domainName = useDomainName();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoadingOpen, setIsLoadingOpen] = useState(false);
  const [domainUserApps, setDomainUserApps] = useState<API.DomainUserAppRead[]>([]);
  const [currentAppIndex, setCurrentAppIndex] = useState<number>(-1);
  const [currentApp, setCurrentApp] = useState<API.AppReadWithApprovedData | undefined>(undefined);
  const [selectValues, setSelectValues] = useState({});
  const formRef = useRef<ProFormInstance>();

  const sleep = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

  const { refresh: reloadDomainUserApps } = useRequest(
    async () => {
      return await usersListAppsBrickapiV1UsersDomainsDomainAppsGet({ domain: domainName || '' });
    },
    {
      // manual: true,
      onSuccess: (data: API.DomainUserAppReadList) => {
        setDomainUserApps(data.results || []);
        // console.log(data);
      },
    },
  );

  const updateDomainUserApp = async (domainUserApp: API.DomainUserAppRead) => {
    const index = findIndex(
      domainUserApps,
      (x: API.DomainUserAppRead) => x.id === domainUserApp.id,
    );
    if (index >= 0) {
      domainUserApps[index] = domainUserApp;
      setDomainUserApps([...domainUserApps]);
    }
    // else {
    //   await reloadDomainUserApps();
    // }
  };

  const onFinish = async (values: any) => {
    if (currentAppIndex >= 0) {
      const currentDomainUserApp = domainUserApps[currentAppIndex];
      const args = fromPairs(map(values.arguments, (x) => [x.name, x.value || '']));
      const result = await usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatch(
        { domain: currentDomainUserApp.domain.name, app: currentDomainUserApp.app.name },
        { arguments: args },
      );
      if (result.errorCode === 'Success' && result.data) {
        await updateDomainUserApp(result.data);
      }
    }
    setIsModalOpen(false);
    setCurrentAppIndex(-1);
  };

  const onCancel = async () => {
    setIsModalOpen(false);
    setCurrentAppIndex(-1);
  };

  const AppCard = (domainUserApp: API.DomainUserAppRead) => {
    const mergeTypes = (...data: any[]) => {
      const types = union(...map(data, keys));
      const result = map(types, (type) => union(...map(data, (x) => get(x, type, []))));
      return zipObject(types, result);
    };

    const parseProfiles = (profiles: API.DomainUserProfileRead[]) => {
      const data = map(profiles, (profile) => {
        const argumentKeys = union(keys(profile.profile.arguments), keys(profile.arguments));
        const argumentValues = map(argumentKeys, (key) => ({
          [profile.profile.arguments[key]]: [profile.arguments[key]],
        }));
        return mergeTypes(...argumentValues);
      });
      return mergeTypes(...data);
    };

    const onClickSettings = async () => {
      setIsLoadingOpen(true);
      const { data: app } = await appsGetBrickapiV1AppsAppGet({ app: domainUserApp.app.name });
      const { data: _domainUserApp } = await usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet({
        domain: domainUserApp.domain.name,
        app: domainUserApp.app.name,
      });
      const index = findIndex(
        domainUserApps,
        (x: API.DomainUserAppRead) => x.id === domainUserApp.id,
      );
      // console.log(_domainUserApp)
      if (app && _domainUserApp && index >= 0) {
        // console.log(app);
        const { data: profiles } =
          await usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGet({
            domain: domainUserApp.domain.name,
          });
        const formTypes = values(app?.approvedData?.permissionProfile?.arguments || {});
        // console.log(formTypes);
        const { data: entities } =
          await usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGet({
            domain: domainUserApp.domain.name,
            types: formTypes,
          });
        const profileTypes = parseProfiles(profiles?.results || []);
        const allTypes = mergeTypes(profileTypes, entities?.read || {}, entities?.write || {});
        // console.log(allTypes);
        setCurrentAppIndex(index);
        setCurrentApp(app);
        setSelectValues(allTypes);
        setIsModalOpen(true);
      } else {
        message.error('can not set arguments');
      }
      setIsLoadingOpen(false);
      // setCurrentDomainUserApp(domainUserApp);
    };

    const operateApp = async (operation: string) => {
      const modal = Modal.info({});
      modal.update({
        title: `${operation === 'start' ? 'Starting' : 'Stopping'} ${domainUserApp.app.name}`,
        content: <Spin />,
        footer: null,
      });
      let result: API.DomainUserAppReadResp;
      if (operation === 'start') {
        result = await usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPost({
          domain: domainUserApp.domain.name,
          app: domainUserApp.app.name,
        });
      } else {
        result = await usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPost({
          domain: domainUserApp.domain.name,
          app: domainUserApp.app.name,
        });
      }
      if (result.errorCode === 'Success' && result.data) {
        let success = false;
        for (let i = 0; i < 10; i++) {
          result = await usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet({
            domain: domainUserApp.domain.name,
            app: domainUserApp.app.name,
          });
          if (result.errorCode === 'Success' && result.data?.status !== domainUserApp.status) {
            success = true;
            break;
          }
          await sleep(500);
        }
        if (!success) {
          message.error(
            `${operation === 'start' ? 'Start' : 'Stop'} ${
              domainUserApp.app.name
            } failed, please try again!`,
          );
        }
        if (result.data) {
          await updateDomainUserApp(result.data);
        }
        modal.destroy();
      }
    };
    const onClickStart = async () => {
      if (domainUserApp.status !== 'running') {
        await operateApp('start');
      }
    };

    const onClickStop = async () => {
      if (domainUserApp.status === 'running') {
        await operateApp('stop');
      }
    };

    const onClickApp = () => {
      const win = window.open(
        `/domain/${domainUserApp.domain.name}/app/${domainUserApp.app.name}`,
        '_blank',
      );
      win?.focus();
      // history.push(`/domain/${domainUserApp.domain.name}/app/${domainUserApp.app.name}`);
    };

    return (
      <Col xxl={6} xl={8} lg={8} md={8} sm={12} xs={24} key={domainUserApp.app.id}>
        <ProCard
          title={domainUserApp.app.name}
          bordered={false}
          actions={[
            <SettingOutlined key="setting" onClick={onClickSettings} />,
            domainUserApp.status !== 'running' ? (
              <PlayCircleOutlined key="start" onClick={onClickStart} />
            ) : (
              <PauseCircleOutlined key="stop" onClick={onClickStop} />
            ),
            <ExportOutlined key="app" onClick={onClickApp} />,
          ]}
        >
          Status: {domainUserApp?.status}
        </ProCard>
      </Col>
    );
  };
  // console.log(currentApp?.approvedData?.permissionProfile?.arguments);

  // if (currentAppIndex >= 0) {
  //
  // }

  const initialValue = map(
    currentApp?.approvedData?.permissionProfile?.arguments || [],
    (value, key) => {
      return {
        name: key,
        type: value,
        value: domainUserApps[currentAppIndex]?.arguments[key] || '',
      };
    },
  );

  console.log(initialValue);
  // formRef?.current?.setFieldsValue(initialValue);

  return (
    <PageContainer>
      <Row gutter={16}>
        {domainUserApps.map((domainUserApp: API.DomainUserAppRead) => AppCard(domainUserApp))}
      </Row>
      <Modal title="Now Loading" open={isLoadingOpen} footer={null} closable={false}>
        <Spin />
      </Modal>
      <ModalForm
        open={isModalOpen}
        title={`app arguments of <${currentApp?.name}>`}
        onFinish={onFinish}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancel,
        }}
        grid
        formRef={formRef}
        // layout="horizontal"
      >
        {!currentApp ? (
          <Spin />
        ) : (
          <ProFormList
            name="arguments"
            // label="Permission Profile Arguments"
            min={initialValue.length}
            max={initialValue.length}
            initialValue={initialValue}
          >
            {(f, index, action) => {
              // console.log(f, index, action);
              return (
                <ProFormGroup key="group">
                  <ProFormText name="name" label="Name" readonly colProps={{ span: 4 }} />
                  <ProFormText name="type" label="Type" readonly colProps={{ span: 8 }} />
                  <ProFormSelect
                    name="value"
                    label="Value"
                    colProps={{ span: 12 }}
                    dependencies={['type']}
                    request={async (params) => {
                      const values = get(selectValues, params.type, []);
                      return map(values, (value) => ({ label: value, value: value }));
                    }}
                  />
                </ProFormGroup>
              );
            }}
          </ProFormList>
        )}
      </ModalForm>
    </PageContainer>
  );
};
export default Dashboard;
