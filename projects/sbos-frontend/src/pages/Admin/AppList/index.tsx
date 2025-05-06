import {
  appsListBrickapiV1AppsGet,
  appsApproveBrickapiV1AppsAppApprovePost,
  appsBuildBrickapiV1AppsAppBuildPost,
} from '@/services/brick-server-playground/apps';
import {useRequest} from '@@/exports';
import {ModalForm, PageContainer, ProFormInstance} from '@ant-design/pro-components';
import {Button, Card, Col, Flex, message, Row, Typography} from 'antd';
import React, {useRef, useState} from 'react';
import hljs from 'highlight.js/lib/core';

const AppList: React.FC = () => {

  const {data: apps, refresh: reloadApps} = useRequest(
    async () => {
      return await appsListBrickapiV1AppsGet({all_apps: true});
    },
    {
      // manual: true,
      onSuccess: (data: API.AppReadResp) => {
        console.log(data);
      },
    },
  );

  const formRef = useRef<ProFormInstance>();
  const [isBuildLogOpen, setIsBuildLogOpen] = useState<boolean>(false);
  const [buildLog, setBuildLog] = useState<string>("");

  const onCloseBuildLog = async () => {
    setIsBuildLogOpen(false);
  }

  const AppCard = (app: API.AppRead) => {
    const handleApproveApp = async () => {
      const result = await appsApproveBrickapiV1AppsAppApprovePost({
        app: app.id,
      });
      console.log(result);
      if (result.errorCode !== "Success") {
        message.error(result.errorCode);
      }

      reloadApps();
    };

    const handleBuildApp = async () => {
      const result = await appsBuildBrickapiV1AppsAppBuildPost({
        app: app.id,
      });
      console.log(result);
      if (result.errorCode === "Success") {
        setBuildLog(result?.data?.stderr || "");
        setIsBuildLogOpen(true);
      } else {
        message.error("Build failed!")
      }
    };


    return (
      <Col xxl={6} xl={8} lg={8} md={8} sm={12} xs={24} key={app.id}>
        <Card title={app.name} bordered={false}>
          <Typography.Paragraph>{app.description}</Typography.Paragraph>
          <Flex gap="middle" wrap>
            {(app.updated || !app.approved) ?
              (<Button type="primary" onClick={handleApproveApp}>
                Approve
              </Button>) : (<Button disabled>Approved</Button>)}
            <Button type="primary" onClick={handleBuildApp}>
              Build
            </Button>
          </Flex>
        </Card>
      </Col>
    );
  };

  return (
    <PageContainer>
      <Row gutter={16}>{apps?.results.map((app: API.AppRead) => AppCard(app))}</Row>
      <ModalForm
        formRef={formRef}
        title="Build Log"
        open={isBuildLogOpen}
        onFinish={onCloseBuildLog}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCloseBuildLog,
          // cancelButtonProps: { hidden: true },
        }}

      >
        <pre>
        <code
          className="hljs"
          dangerouslySetInnerHTML={{
            __html: hljs.highlight('plaintext', buildLog).value,
          }}
        />
        </pre>
      </ModalForm>
    </PageContainer>
  );
};

export default AppList;
