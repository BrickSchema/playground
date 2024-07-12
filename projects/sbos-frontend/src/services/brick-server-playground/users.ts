// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Users:List Users GET /brickapi/v1/users/ */
export async function usersListUsersBrickapiV1UsersGet(options?: { [key: string]: any }) {
  return request<API.UserReadListResp>('/brickapi/v1/users/', {
    method: 'GET',
    ...(options || {}),
  });
}

/** Users:User GET /brickapi/v1/users/${param0} */
export async function usersUserBrickapiV1UsersUserGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersUserBrickapiV1UsersUserGetParams,
  options?: { [key: string]: any },
) {
  const { user: param0, ...queryParams } = params;
  return request<API.UserReadResp>(`/brickapi/v1/users/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Delete User DELETE /brickapi/v1/users/${param0} */
export async function usersDeleteUserBrickapiV1UsersUserDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersDeleteUserBrickapiV1UsersUserDeleteParams,
  options?: { [key: string]: any },
) {
  const { user: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/users/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Patch User PATCH /brickapi/v1/users/${param0} */
export async function usersPatchUserBrickapiV1UsersUserPatch(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersPatchUserBrickapiV1UsersUserPatchParams,
  body: API.UserUpdate,
  options?: { [key: string]: any },
) {
  const { user: param0, ...queryParams } = params;
  return request<API.UserReadResp>(`/brickapi/v1/users/${param0}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Users:List Apps View apps that user activated in a domain. GET /brickapi/v1/users/domains/${param0}/apps */
export async function usersListAppsBrickapiV1UsersDomainsDomainAppsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListAppsBrickapiV1UsersDomainsDomainAppsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserAppReadListResp>(`/brickapi/v1/users/domains/${param0}/apps`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:List Apps View apps that user activated in a domain. GET /brickapi/v1/users/domains/${param0}/apps */
export async function usersListAppsBrickapiV1UsersDomainsDomainAppsGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListAppsBrickapiV1UsersDomainsDomainAppsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserAppReadListResp>(`/brickapi/v1/users/domains/${param0}/apps`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Get App Get an app for the user. GET /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersGetAppBrickapiV1UsersDomainsDomainAppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Get App Get an app for the user. GET /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersGetAppBrickapiV1UsersDomainsDomainAppsAppGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersGetAppBrickapiV1UsersDomainsDomainAppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Install App Get an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Install App Get an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Uninstall App Uninstall an app for the user. DELETE /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Uninstall App Uninstall an app for the user. DELETE /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Users:Set App Arguments Set the arguments of an app for the user. PATCH /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatch(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatchParams,
  body: API.DomainUserAppArguments,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Users:Set App Arguments Set the arguments of an app for the user. PATCH /brickapi/v1/users/domains/${param0}/apps/${param1} */
export async function usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatch2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatchParams,
  body: API.DomainUserAppArguments,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(`/brickapi/v1/users/domains/${param0}/apps/${param1}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Users:Create App Container Create the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/create */
export async function usersCreateAppContainerBrickapiV1UsersDomainsDomainAppsAppCreatePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersCreateAppContainerBrickapiV1UsersDomainsDomainAppsAppCreatePostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/create`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Create App Container Create the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/create */
export async function usersCreateAppContainerBrickapiV1UsersDomainsDomainAppsAppCreatePost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersCreateAppContainerBrickapiV1UsersDomainsDomainAppsAppCreatePostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/create`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Remove App Container Remove the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/remove */
export async function usersRemoveAppContainerBrickapiV1UsersDomainsDomainAppsAppRemovePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersRemoveAppContainerBrickapiV1UsersDomainsDomainAppsAppRemovePostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/remove`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Remove App Container Remove the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/remove */
export async function usersRemoveAppContainerBrickapiV1UsersDomainsDomainAppsAppRemovePost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersRemoveAppContainerBrickapiV1UsersDomainsDomainAppsAppRemovePostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/remove`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Start App Container Start the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/start */
export async function usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/start`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Start App Container Start the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/start */
export async function usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/start`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Stop App Container Stop the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/stop */
export async function usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/stop`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Stop App Container Stop the container of an app for the user. POST /brickapi/v1/users/domains/${param0}/apps/${param1}/stop */
export async function usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainUserAppReadResp>(
    `/brickapi/v1/users/domains/${param0}/apps/${param1}/stop`,
    {
      method: 'POST',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:List Domain Permissions Get all authorized permissions of the token in domain. GET /brickapi/v1/users/domains/${param0}/permissions */
export async function usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.AuthorizedEntitiesResp>(`/brickapi/v1/users/domains/${param0}/permissions`, {
    method: 'GET',
    params: {
      ...queryParams,
    },
    ...(options || {}),
  });
}

/** Users:List Domain Permissions Get all authorized permissions of the token in domain. GET /brickapi/v1/users/domains/${param0}/permissions */
export async function usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.AuthorizedEntitiesResp>(`/brickapi/v1/users/domains/${param0}/permissions`, {
    method: 'GET',
    params: {
      ...queryParams,
    },
    ...(options || {}),
  });
}

/** Users:List Domain User Profiles GET /brickapi/v1/users/domains/${param0}/profiles */
export async function usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserProfileReadListResp>(
    `/brickapi/v1/users/domains/${param0}/profiles`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:List Domain User Profiles GET /brickapi/v1/users/domains/${param0}/profiles */
export async function usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserProfileReadListResp>(
    `/brickapi/v1/users/domains/${param0}/profiles`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Users:Init Superuser Set the current user as superuser. Can only be called when there is no superuser in the site. POST /brickapi/v1/users/init_superuser */
export async function usersInitSuperuserBrickapiV1UsersInitSuperuserPost(options?: {
  [key: string]: any;
}) {
  return request<API.UserReadResp>('/brickapi/v1/users/init_superuser', {
    method: 'POST',
    ...(options || {}),
  });
}

/** Users:Current User GET /brickapi/v1/users/me */
export async function usersCurrentUserBrickapiV1UsersMeGet(options?: { [key: string]: any }) {
  return request<API.UserReadResp>('/brickapi/v1/users/me', {
    method: 'GET',
    ...(options || {}),
  });
}

/** Users:Patch Current User PATCH /brickapi/v1/users/me */
export async function usersPatchCurrentUserBrickapiV1UsersMePatch(
  body: API.UserUpdate,
  options?: { [key: string]: any },
) {
  return request<API.UserReadResp>('/brickapi/v1/users/me', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}
