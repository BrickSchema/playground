import { useDomainName } from '@/hooks';
import UserProfiles from '@/pages/Domain/UserList/profile';
import {
  addDomainUserBrickapiV1DomainsDomainUsersUserPost,
  addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPost,
  deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDelete,
  listDomainUserBrickapiV1DomainsDomainUsersGet,
  updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatch,
} from '@/services/brick-server-playground/domains';
import { listProfilesBrickapiV1ProfilesGet } from '@/services/brick-server-playground/profiles';
import { usersListUsersBrickapiV1UsersGet } from '@/services/brick-server-playground/users';
import { PlusOutlined } from '@ant-design/icons';
import {
  ActionType,
  ModalForm,
  PageContainer,
  ProCard,
  ProColumns,
  ProFormGroup,
  ProFormList,
  ProFormSelect,
  ProFormText,
  ProTable,
} from '@ant-design/pro-components';
import { Button, Col, Popconfirm, Row, message } from 'antd';
import hljs from 'highlight.js/lib/core';
import { filter, fromPairs, map } from 'lodash';
import React, { RefObject, useRef, useState } from 'react';

const UserList: React.FC = () => {
  const domainName = useDomainName();
  const actionRef = useRef<ActionType>();
  const [isAddUserOpen, setIsAddUserOpen] = useState<boolean>(false);
  const [isEditProfileOpen, setIsEditProfileOpen] = useState<boolean>(false);
  const [isAddProfileOpen, setIsAddProfileOpen] = useState<boolean>(false);
  const [currentProfile, setCurrentProfile] = useState<API.DomainUserProfileRead | undefined>(
    undefined,
  );
  const [currentDomainUser, setCurrentDomainUser] = useState<API.DomainUserRead | undefined>(
    undefined,
  );
  const [profileActionRef, setProfileActionRef] = useState<RefObject<ActionType> | undefined>(
    undefined,
  );

  const onClickAddUser = async () => {
    setIsAddUserOpen(true);
  };

  const onFinishAddUser = async (params: { user: string }) => {
    const result = await addDomainUserBrickapiV1DomainsDomainUsersUserPost({
      domain: domainName,
      user: params.user,
    });
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    setIsAddUserOpen(false);
    actionRef.current?.reload();
  };

  const onCancelAddUser = async () => {
    setIsAddUserOpen(false);
  };
  const onClickEditProfile = async (
    profile: API.DomainUserProfileRead,
    profileActionRef: RefObject<ActionType>,
  ) => {
    setCurrentProfile(profile);
    setProfileActionRef(profileActionRef);
    setIsEditProfileOpen(true);
  };

  const onClickDeleteProfile = async (
    profile: API.DomainUserProfileRead,
    profileActionRef: RefObject<ActionType>,
  ) => {
    await deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDelete({
      domain: domainName,
      user: profile.user.name,
      profile: profile.profile.id,
    });
    profileActionRef?.current?.reload();
  };
  const onFinishEditProfile = async (values: any) => {
    const args = fromPairs(map(values.arguments, (x) => [x.name, x.value || '']));
    const result =
      await updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatch(
        {
          domain: domainName,
          user: currentProfile?.user.name || '',
          profile: currentProfile?.profile.id || '',
        },
        { arguments: args },
      );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    profileActionRef?.current?.reload();
    setIsEditProfileOpen(false);
  };

  const onCancelEditProfile = async () => {
    setIsEditProfileOpen(false);
  };

  const onClickAddProfile = async (
    domainUser: API.DomainUserRead,
    profileActionRef: RefObject<ActionType>,
  ) => {
    setCurrentDomainUser(domainUser);
    setProfileActionRef(profileActionRef);
    setIsAddProfileOpen(true);
  };

  const onFinishAddProfile = async (params: { profile: string }) => {
    const result = await addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPost(
      { domain: domainName, user: currentDomainUser?.user.name || '' },
      { profile: params.profile },
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    profileActionRef?.current?.reload();
    setIsAddProfileOpen(false);
  };

  const onCancelAddProfile = async () => {
    setIsAddProfileOpen(false);
  };

  const columns: ProColumns<API.DomainUserRead>[] = [
    {
      title: 'User',
      dataIndex: 'name',
      render: (_, record) => <span>{record.user.name}</span>,
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        // <a key="add_profile" onClick={() => onClickAddProfile(record)}>Add Profile</a>,
        <Popconfirm
          key="delete"
          title="Delete the user"
          description="Are you sure to delete this user?"
          onConfirm={async () => {}}
        >
          <a>Delete</a>
        </Popconfirm>,
      ],
    },
  ];
  const expandedRowRender = (domainUser: API.DomainUserRead) => {
    return (
      <UserProfiles
        domainUser={domainUser}
        onClickDeleteProfile={onClickDeleteProfile}
        onClickEditProfile={onClickEditProfile}
        onClickAddProfile={onClickAddProfile}
      />
    );
  };

  const initialValue = map(currentProfile?.profile.arguments || [], (value, key) => {
    return {
      name: key,
      type: value,
      value: currentProfile?.arguments[key] || '',
    };
  });

  return (
    <PageContainer>
      <ProTable<API.DomainUserRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        expandable={{ expandedRowRender }}
        request={async (params, sort, filter) => {
          const result = await listDomainUserBrickapiV1DomainsDomainUsersGet({
            domain: domainName,
          });
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={onClickAddUser}>
            Add User
          </Button>,
        ]}
      />
      <ModalForm
        title={'Add User to Domain'}
        open={isAddUserOpen}
        onFinish={onFinishAddUser}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelAddUser,
        }}
      >
        <ProFormSelect
          label="Select a user"
          name="user"
          request={async () => {
            const result = await usersListUsersBrickapiV1UsersGet();
            return map(result.data?.results || [], (user) => ({
              value: user.name,
              label: user.name,
            }));
          }}
          rules={[
            {
              required: true,
              message: 'Please select a user.',
            },
          ]}
        />
      </ModalForm>
      <ModalForm
        title="Set Profile Arguments"
        open={isEditProfileOpen}
        onFinish={onFinishEditProfile}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelEditProfile,
        }}
        grid
      >
        <Row>
          <Col span={12}>
            <ProCard title="Read">
              <code
                className="hljs"
                dangerouslySetInnerHTML={{
                  __html: hljs.highlight('sparql', currentProfile?.profile.read || '').value,
                }}
              />
            </ProCard>
          </Col>
          <Col span={12}>
            <ProCard title="Read + Write">
              <code
                className="hljs"
                dangerouslySetInnerHTML={{
                  __html: hljs.highlight('sparql', currentProfile?.profile.write || '').value,
                }}
              />
            </ProCard>
          </Col>
          <Col span={24}>
            <ProCard title="Arguments">
              <ProFormList
                name="arguments"
                min={initialValue.length}
                max={initialValue.length}
                initialValue={initialValue}
              >
                <ProFormGroup key="group">
                  <ProFormText name="name" label="Name" readonly colProps={{ span: 4 }} />
                  <ProFormText name="type" label="Type" readonly colProps={{ span: 8 }} />
                  <ProFormText name="value" label="Value" colProps={{ span: 12 }} />
                </ProFormGroup>
              </ProFormList>
            </ProCard>
          </Col>
        </Row>
      </ModalForm>
      <ModalForm
        title="Add Profile"
        open={isAddProfileOpen}
        onFinish={onFinishAddProfile}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelAddProfile,
        }}
      >
        <ProFormSelect
          label="Select a profile"
          name="profile"
          request={async () => {
            const result = await listProfilesBrickapiV1ProfilesGet();
            return map(
              filter(result.data?.results || [], (x) => x.name),
              (profile: API.PermissionProfileRead) => ({
                value: profile.id,
                label: profile.name,
              }),
            );
          }}
          rules={[
            {
              required: true,
              message: 'Please select a profile.',
            },
          ]}
        />
      </ModalForm>
    </PageContainer>
  );
};

export default UserList;
