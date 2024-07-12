import { useDomainName } from '@/hooks';
import { getActuationGuardsBrickapiV1ActuationGuardsGet } from '@/services/brick-server-playground/actuation';
import {
  createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPost,
  deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDelete,
  listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGet,
  updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatch,
} from '@/services/brick-server-playground/domains';
import { postBrickapiV1DomainsDomainSparqlPost } from '@/services/brick-server-playground/queries';
import { PlusOutlined } from '@ant-design/icons';
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
import { Button, Popconfirm, Tag, message } from 'antd';
import hljs from 'highlight.js/lib/core';
import { map } from 'lodash';
import React, { useRef, useState } from 'react';

const PolicyList: React.FC = () => {
  const domainName = useDomainName();
  const actionRef = useRef<ActionType>();
  const formRef = useRef<ProFormInstance>();

  const [currentPolicy, setCurrentPolicy] = useState<API.DomainPreActuationPolicyRead | undefined>(
    undefined,
  );
  const [queryResult, setQueryResult] = useState<any>({});
  const [isEditPolicyOpen, setIsEditPolicyOpen] = useState<boolean>(false);

  const onClickAddPolicy = async () => {
    setCurrentPolicy(undefined);
    setQueryResult({});
    setIsEditPolicyOpen(true);
  };

  const onClickEditPolicy = async (policy: API.DomainPreActuationPolicyRead) => {
    setCurrentPolicy(policy);
    setQueryResult({});
    setIsEditPolicyOpen(true);
  };

  const onFinishAddPolicy = async (values: {
    name: string;
    query: string;
    priority: number;
    guards: string[];
  }) => {
    console.log(values);
    let result;
    if (currentPolicy) {
      result = await updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatch(
        { domain: domainName, policy: currentPolicy.id },
        values,
      );
    } else {
      result = await createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPost(
        { domain: domainName },
        values,
      );
    }
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      await actionRef.current?.reload();
      setCurrentPolicy(undefined);
      setQueryResult({});
      setIsEditPolicyOpen(false);
    }
  };

  const onCancelEditPolicy = async () => {
    setCurrentPolicy(undefined);
    setQueryResult({});
    setIsEditPolicyOpen(false);
  };

  const onDeletePolicy = async (policy: API.DomainPreActuationPolicyRead) => {
    const result = await deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDelete({
      domain: domainName,
      policy: policy.id,
    });
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    await actionRef.current?.reload();
  };

  const onClickRunQuery = async () => {
    const query = formRef.current?.getFieldValue('query') || '';
    if (query) {
      const res = await postBrickapiV1DomainsDomainSparqlPost({ domain: domainName }, query);
      setQueryResult(res);
      console.log(JSON.stringify(res.data, undefined, 2));
    }
  };

  const columns: ProColumns<API.DomainPreActuationPolicyRead>[] = [
    {
      title: 'Name',
      dataIndex: 'name',
    },
    {
      title: 'Guards',
      dataIndex: 'guards',
      render: (_, record) => (
        <>
          {record.guards.map((guard) => (
            <Tag>{guard}</Tag>
          ))}
        </>
      ),
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="add_profile" onClick={() => onClickEditPolicy(record)}>
          Edit
        </a>,
        <Popconfirm
          key="delete"
          title="Delete the Pre Acutuation Policy"
          description="Are you sure to delete this pre actuation policy?"
          onConfirm={async () => onDeletePolicy(record)}
        >
          <a>Delete</a>
        </Popconfirm>,
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable<API.DomainPreActuationPolicyRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        request={async (params, sort, filter) => {
          const result = await listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGet({
            domain: domainName,
          });
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={onClickAddPolicy}>
            Add Policy
          </Button>,
        ]}
      />
      <ModalForm
        formRef={formRef}
        title={`${currentPolicy ? 'Edit' : 'Add'} Domain Pre Actuation Policy`}
        open={isEditPolicyOpen}
        onFinish={onFinishAddPolicy}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelEditPolicy,
        }}
      >
        <ProFormText
          label="Name"
          name="name"
          initialValue={currentPolicy?.name || ''}
          rules={[
            {
              required: true,
              message: 'Please enter name.',
            },
          ]}
        />
        <ProFormTextArea
          label="Query"
          name="query"
          initialValue={currentPolicy?.query || ''}
          rules={[
            {
              required: true,
              message: 'Please enter query.',
            },
          ]}
        />
        <ProFormText
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
        </ProFormText>
        <ProFormDigit
          label="Priority"
          name="priority"
          fieldProps={{ precision: 0 }}
          initialValue={currentPolicy?.priority || 0}
          rules={[
            {
              required: true,
              message: 'Please enter priority.',
            },
          ]}
        />
        <ProFormSelect
          label="Guards"
          name="guards"
          mode="multiple"
          initialValue={currentPolicy?.guards || []}
          request={async () => {
            const result = await getActuationGuardsBrickapiV1ActuationGuardsGet();
            return map(result.data?.results || [], (guard) => ({
              value: guard,
              label: guard,
            }));
          }}
          rules={[
            {
              required: true,
              message: 'Please select guards.',
            },
          ]}
        />
      </ModalForm>
    </PageContainer>
  );
};

export default PolicyList;
