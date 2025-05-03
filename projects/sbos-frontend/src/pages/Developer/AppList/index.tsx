import {useDomainName} from '@/hooks';
import {
  appsListBrickapiV1AppsGet,
  appsRegistrationBrickapiV1AppsPost,
  appsGetBrickapiV1AppsAppGet,
  appsSubmitDataBrickapiV1AppsAppSubmitPost,
} from '@/services/brick-server-playground/apps';
import {
  domainApproveAppBrickapiV1DomainsDomainAppsAppPost,
  domainListAppBrickapiV1DomainsDomainAppsGet,
} from '@/services/brick-server-playground/domains';
import {useRequest} from '@@/exports';
import {
  ActionType,
  ModalForm,
  PageContainer,
  ProColumns,
  ProFormInstance, ProFormSelect,
  ProFormText, ProFormTextArea, ProFormUploadButton,
  ProTable
} from '@ant-design/pro-components';
import {Button, Card, Col, message, Row, Typography} from 'antd';
import React, {useRef, useState} from 'react';
import {
  createProfileBrickapiV1ProfilesPost, listProfilesBrickapiV1ProfilesGet,
  updateProfileBrickapiV1ProfilesProfilePost
} from "@/services/brick-server-playground/profiles";
import {PlusOutlined} from "@ant-design/icons";

const AppList: React.FC = () => {
  /*  const domainName = useDomainName();

    const { data: apps, refresh: reloadApps } = useRequest(
      async () => {
        return await appsListBrickapiV1AppsGet({});
      },
      {
        // manual: true,
        onSuccess: (data: API.AppReadResp) => {
          console.log(data);
        },
      },
    );


    const AppCard = (app: API.AppRead) => {
      return (
        <Col xxl={6} xl={8} lg={8} md={8} sm={12} xs={24} key={app.id}>
          <Card title={app.name} bordered={false}>
            <Typography.Paragraph>{app.description}</Typography.Paragraph>
          </Card>
        </Col>
      );
    };

    return (
      <PageContainer>
        <Row gutter={16}>{apps?.results.map((app: API.AppRead) => AppCard(app))}</Row>
      </PageContainer>
    );*/

  const actionRef = useRef<ActionType>();
  const registerFormRef = useRef<ProFormInstance>();
  const submitFormRef = useRef<ProFormInstance>();

  const [currentApp, setCurrentApp] = useState<API.AppReadWithAllData | undefined>(
    undefined,
  );
  const [queryResult, setQueryResult] = useState<any>({});
  const [isRegisterAppOpen, setIsRegisterAppOpen] = useState<boolean>(false);
  const [isSubmitAppOpen, setIsSubmitAppOpen] = useState<boolean>(false);

  const onClickRegisterApp = async () => {
    setCurrentApp(undefined);
    setQueryResult({});
    setIsRegisterAppOpen(true);
  };

  const onClickSubmitApp = async (app: API.AppRead) => {
    const result = await appsGetBrickapiV1AppsAppGet({app: app.name});
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
      return;
    }
    setCurrentApp(result.data || undefined);
    setQueryResult({});
    setIsSubmitAppOpen(true);
  };

  const onFinishRegisterApp = async (values: {
    name: string;
    description: string;
  }) => {
    console.log(values);
    const result = await appsRegistrationBrickapiV1AppsPost(values);
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      await actionRef.current?.reload();
      setCurrentApp(undefined);
      setQueryResult({});
      setIsRegisterAppOpen(false);
    }
  };

  const onFinishSubmitApp = async (values: {
    frontend_file: any,
    backend_file: any,
    permission_profile_read: string;
    permission_profile_write: string;
    permission_profile_arguments: string | any;
    permission_model: API.PermissionModel;
  }) => {
    values.permission_profile_arguments = JSON.parse(values.permission_profile_arguments);
    values.frontend_file = values.frontend_file[0].originFileObj;
    values.backend_file = values.backend_file[0].originFileObj;
    console.log(values);
    const result = await appsSubmitDataBrickapiV1AppsAppSubmitPost(
      {app: currentApp?.name || ""},
      values,
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      await actionRef.current?.reload();
      setCurrentApp(undefined);
      setQueryResult({});
      setIsSubmitAppOpen(false);
    }
  };

  const onCancel = async () => {
    setCurrentApp(undefined);
    setQueryResult({});
    setIsRegisterAppOpen(false);
    setIsSubmitAppOpen(false);
  };

  // const onDeletePolicy = async (policy: API.DomainPreActuationPolicyRead) => {
  //   const result = await deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDelete({
  //     domain: domainName,
  //     policy: policy.id,
  //   });
  //   if (result.errorCode !== 'Success') {
  //     message.error(`Error: ${result.errorCode}`);
  //   }
  //   await actionRef.current?.reload();
  // };
  //
  // const onClickRunQuery = async () => {
  //   const query = formRef.current?.getFieldValue('query') || '';
  //   if (query) {
  //     const res = await postBrickapiV1DomainsDomainSparqlPost({domain: domainName}, query);
  //     setQueryResult(res);
  //     console.log(JSON.stringify(res.data, undefined, 2));
  //   }
  // };

  const columns: ProColumns<API.AppRead>[] = [
    {
      title: 'Name',
      dataIndex: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="add_profile" onClick={() => onClickSubmitApp(record)}>
          Submit new version
        </a>,
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable<API.AppRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        request={async (params, sort, filter) => {
          const result = await appsListBrickapiV1AppsGet({});
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined/>} onClick={onClickRegisterApp}>
            Register App
          </Button>,
        ]}
      />
      <ModalForm
        formRef={registerFormRef}
        title={`Register App`}
        open={isRegisterAppOpen}
        onFinish={onFinishRegisterApp}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancel,
        }}
      >
        <ProFormText
          label="Name"
          name="name"
          initialValue=""
          rules={[
            {
              required: true,
              message: 'Please enter name.',
            },
          ]}
        />
        <ProFormText
          label="Description"
          name="description"
          initialValue=""
          rules={[
            {
              required: true,
              message: 'Please enter description.',
            },
          ]}
        />
      </ModalForm>
      <ModalForm
        formRef={submitFormRef}
        title={`Submit New Version`}
        open={isSubmitAppOpen}
        onFinish={onFinishSubmitApp}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancel,
        }}
      >
        <ProFormText
          label="Name"
          name="name"
          initialValue={currentApp?.name || ''}
          disabled
        />
        <ProFormText
          label="Description"
          name="description"
          initialValue={currentApp?.description || ''}
          disabled
        />
        <ProFormUploadButton
          label="Frontend Zip File"
          title="Select a file"
          name="frontend_file"
          max={1}
          accept=".zip"
          rules={[
            {
              required: true,
              message: 'Please choose a file.',
            },
          ]}
        />
        <ProFormUploadButton
          label="Backend Zip File"
          title="Select a file"
          name="backend_file"
          max={1}
          accept=".zip"
          rules={[
            {
              required: true,
              message: 'Please choose a file.',
            },
          ]}
        />
        <ProFormTextArea
          label="Permission Profile Read"
          name="permission_profile_read"
          initialValue={currentApp?.submittedData?.permissionProfile?.read || ''}
          rules={[
            {
              required: true,
              message: 'Please enter read query.',
            },
          ]}
        />
        <ProFormTextArea
          label="Permission Profile Write"
          name="permission_profile_write"
          initialValue={currentApp?.submittedData?.permissionProfile?.write || ''}
          rules={[
            {
              required: true,
              message: 'Please enter write query.',
            },
          ]}
        />
        <ProFormTextArea
          label="Arguments (JSON format)"
          name="permission_profile_arguments"
          initialValue={currentApp?.submittedData?.permissionProfile?.arguments && JSON.stringify(currentApp?.submittedData?.permissionProfile?.arguments) || ''}
          rules={[
            {
              required: true,
              message: 'Please enter arguments.',
            },
          ]}
        />
        <ProFormSelect
          label="Deligation Schema"
          name="permission_model"
          initialValue={currentApp?.submittedData?.permissionModel || ''}
          valueEnum={{
            intersection: 'Intersection',
            augmentation: 'Augmentation',
          }}
          rules={[{required: true, message: 'Please select a deligation schema'}]}
        />
      </ModalForm>
    </PageContainer>
  )

};

export default AppList;
