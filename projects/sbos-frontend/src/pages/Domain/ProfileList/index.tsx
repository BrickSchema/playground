import {useDomainName} from '@/hooks';
// import {postBrickapiV1DomainsDomainSparqlPost} from '@/services/brick-server-playground/queries';
import {
  createProfileBrickapiV1ProfilesPost,
  getProfileBrickapiV1ProfilesProfileGet,
  listProfilesBrickapiV1ProfilesGet,
  updateProfileBrickapiV1ProfilesProfilePost
} from '@/services/brick-server-playground/profiles'
import {PlusOutlined} from '@ant-design/icons';
import {
  ActionType,
  ModalForm,
  PageContainer,
  ProColumns,
  ProFormDigit,
  ProFormInstance,
  ProFormSelect,
  ProFormText,
  ProFormTextArea,
  ProTable,
} from '@ant-design/pro-components';
import {Button, Popconfirm, Tag, message} from 'antd';
import hljs from 'highlight.js/lib/core';
import {map} from 'lodash';
import React, {useRef, useState} from 'react';

const ProfileList: React.FC = () => {
  const domainName = useDomainName();
  const actionRef = useRef<ActionType>();
  const formRef = useRef<ProFormInstance>();

  const [currentProfile, setCurrentProfile] = useState<API.PermissionProfileRead | undefined>(
    undefined,
  );
  const [queryResult, setQueryResult] = useState<any>({});
  const [isEditPolicyOpen, setIsEditPolicyOpen] = useState<boolean>(false);

  const onClickAddProfile = async () => {
    setCurrentProfile(undefined);
    setQueryResult({});
    setIsEditPolicyOpen(true);
  };

  const onClickEditProfile = async (profile: API.PermissionProfileRead) => {
    setCurrentProfile(profile);
    setQueryResult({});
    setIsEditPolicyOpen(true);
  };

  const onFinishAddProfile = async (values: {
    name: string;
    read: string;
    write: string;
    arguments: string | any;
  }) => {
    values.arguments = JSON.parse(values.arguments);
    console.log(values);
    let result;
    if (currentProfile) {
      result = await updateProfileBrickapiV1ProfilesProfilePost(
        {profile: currentProfile.id},
        values,
      );
    } else {
      result = await createProfileBrickapiV1ProfilesPost(
        values,
      );
    }
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      await actionRef.current?.reload();
      setCurrentProfile(undefined);
      setQueryResult({});
      setIsEditPolicyOpen(false);
    }
  };

  const onCancelEditPolicy = async () => {
    setCurrentProfile(undefined);
    setQueryResult({});
    setIsEditPolicyOpen(false);
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

  const columns: ProColumns<API.PermissionProfileRead>[] = [
    {
      title: 'Name',
      dataIndex: 'name',
    },
    {
      title: 'Read',
      dataIndex: 'read',
    },
    {
      title: 'Write',
      dataIndex: 'write',
    },
    {
      title: 'Arguments',
      dataIndex: 'arguments',
      render: (_, record) => (
        <>
          {JSON.stringify(record.arguments)}
        </>
      )
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="add_profile" onClick={() => onClickEditProfile(record)}>
          Edit
        </a>,
        // <Popconfirm
        //   key="delete"
        //   title="Delete the Pre Acutuation Policy"
        //   description="Are you sure to delete this pre actuation policy?"
        //   onConfirm={async () => onDeletePolicy(record)}
        // >
        //   <a>Delete</a>
        // </Popconfirm>,
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable<API.PermissionProfileRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        request={async (params, sort, filter) => {
          const result = await listProfilesBrickapiV1ProfilesGet({type: "user"});
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined/>} onClick={onClickAddProfile}>
            Add Profile
          </Button>,
        ]}
      />
      <ModalForm
        formRef={formRef}
        title={`${currentProfile ? 'Edit' : 'Add'} Profile`}
        open={isEditPolicyOpen}
        onFinish={onFinishAddProfile}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelEditPolicy,
        }}
      >
        <ProFormText
          label="Name"
          name="name"
          initialValue={currentProfile?.name || ''}
          rules={[
            {
              required: true,
              message: 'Please enter name.',
            },
          ]}
        />
        <ProFormTextArea
          label="Permission Profile Read"
          name="read"
          initialValue={currentProfile?.read || ''}
          rules={[
            {
              required: true,
              message: 'Please enter read query.',
            },
          ]}
        />
        <ProFormTextArea
          label="Permission Profile Write"
          name="write"
          initialValue={currentProfile?.write || ''}
          rules={[
            {
              required: true,
              message: 'Please enter write query.',
            },
          ]}
        />
        {/*<ProFormText
          label={
            <Button type="primary" onClick={onClickRunQuery}>
              Run Query
            </Button>
          }
          fieldProps={{ style: { display: 'none' } }}
        >
          {queryResult?.errorCode === 'Success' ? (
            <pre>
              <code
                className="hljs"
                dangerouslySetInnerHTML={{
                  __html: hljs.highlight('json', JSON.stringify(queryResult.data, undefined, 2))
                    .value,
                }}
              />
            </pre>
          ) : (
            <span>{queryResult?.errorCode || 'No query result'}</span>
          )}
        </ProFormText>*/}
        <ProFormTextArea
          label="Arguments (JSON format)"
          name="arguments"
          initialValue={currentProfile?.arguments && JSON.stringify(currentProfile?.arguments) || ''}
          rules={[
            {
              required: true,
              message: 'Please enter arguments.',
            },
          ]}
        />
      </ModalForm>
    </PageContainer>
  )

}

export default ProfileList;
