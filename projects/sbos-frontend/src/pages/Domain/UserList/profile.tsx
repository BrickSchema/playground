import { useDomainName } from '@/hooks';
import { listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGet } from '@/services/brick-server-playground/domains';
import { PlusOutlined } from '@ant-design/icons';
import { ActionType, ProColumns, ProTable } from '@ant-design/pro-components';
import { Button, Popconfirm } from 'antd';
import React, { useRef } from 'react';

interface UserProfileProps {
  domainUser: API.DomainUserRead;
  onClickDeleteProfile: any;
  onClickEditProfile: any;
  onClickAddProfile: any;
}

const UserProfiles: React.FC<UserProfileProps> = ({
  domainUser,
  onClickDeleteProfile,
  onClickEditProfile,
  onClickAddProfile,
}) => {
  const domainName = useDomainName();
  const actionRef = useRef<ActionType>();

  const profileColumns: ProColumns<API.DomainUserProfileRead>[] = [
    {
      dataIndex: 'index',
      valueType: 'indexBorder',
      width: 48,
    },
    {
      title: 'Profile',
      dataIndex: 'name',
      render: (_, record) => <span>{record.profile.name}</span>,
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="edit" onClick={() => onClickEditProfile(record, actionRef)}>
          Edit
        </a>,
        <Popconfirm
          key="delete"
          title="Delete the profile"
          description="Are you sure to delete this profile?"
          onConfirm={() => onClickDeleteProfile(record, actionRef)}
        >
          <a>Delete</a>
        </Popconfirm>,
      ],
    },
    {
      title: (
        <Button
          key="add"
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => onClickAddProfile(domainUser, actionRef)}
        >
          Add Profile
        </Button>
      ),
      width: 48,
    },
  ];

  return (
    <ProTable<API.DomainUserProfileRead>
      actionRef={actionRef}
      columns={profileColumns}
      headerTitle={false}
      search={false}
      options={false}
      pagination={false}
      request={async (params, sort, filter) => {
        const result = await listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGet({
          domain: domainName,
          user: domainUser.user.id,
        });
        return {
          data: result.data?.results || [],
          success: true,
          total: result.data?.count || 0,
        };
      }}
    />
  );
};

export default UserProfiles;
