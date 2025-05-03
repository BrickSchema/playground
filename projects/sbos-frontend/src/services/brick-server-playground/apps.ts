// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Apps:List Get all apps on the site. GET /brickapi/v1/apps/ */
export async function appsListBrickapiV1AppsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsListBrickapiV1AppsGetParams,
  options?: { [key: string]: any },
) {
  return request<API.AppReadListResp>('/brickapi/v1/apps/', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Apps:List Get all apps on the site. GET /brickapi/v1/apps/ */
export async function appsListBrickapiV1AppsGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsListBrickapiV1AppsGetParams,
  options?: { [key: string]: any },
) {
  return request<API.AppReadListResp>('/brickapi/v1/apps/', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Apps:Registration Register an app. POST /brickapi/v1/apps/ */
export async function appsRegistrationBrickapiV1AppsPost(
  body: API.AppCreate,
  options?: { [key: string]: any },
) {
  return request<API.AppReadResp>('/brickapi/v1/apps/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Apps:Registration Register an app. POST /brickapi/v1/apps/ */
export async function appsRegistrationBrickapiV1AppsPost2(
  body: API.AppCreate,
  options?: { [key: string]: any },
) {
  return request<API.AppReadResp>('/brickapi/v1/apps/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Apps:Get Get information about an app. GET /brickapi/v1/apps/${param0} */
export async function appsGetBrickapiV1AppsAppGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsGetBrickapiV1AppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppReadWithAllDataResp>(`/brickapi/v1/apps/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Get Get information about an app. GET /brickapi/v1/apps/${param0} */
export async function appsGetBrickapiV1AppsAppGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsGetBrickapiV1AppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppReadWithAllDataResp>(`/brickapi/v1/apps/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Delete Delete an app (site admin). DELETE /brickapi/v1/apps/${param0} */
export async function appsDeleteBrickapiV1AppsAppDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsDeleteBrickapiV1AppsAppDeleteParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/apps/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Delete Delete an app (site admin). DELETE /brickapi/v1/apps/${param0} */
export async function appsDeleteBrickapiV1AppsAppDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsDeleteBrickapiV1AppsAppDeleteParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/apps/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Approve Approve an app (site admin). POST /brickapi/v1/apps/${param0}/approve */
export async function appsApproveBrickapiV1AppsAppApprovePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApproveBrickapiV1AppsAppApprovePostParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppReadWithApprovedDataResp>(`/brickapi/v1/apps/${param0}/approve`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Approve Approve an app (site admin). POST /brickapi/v1/apps/${param0}/approve */
export async function appsApproveBrickapiV1AppsAppApprovePost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApproveBrickapiV1AppsAppApprovePostParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppReadWithApprovedDataResp>(`/brickapi/v1/apps/${param0}/approve`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Build Build an app (site admin). POST /brickapi/v1/apps/${param0}/build */
export async function appsBuildBrickapiV1AppsAppBuildPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsBuildBrickapiV1AppsAppBuildPostParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppBuildResp>(`/brickapi/v1/apps/${param0}/build`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Build Build an app (site admin). POST /brickapi/v1/apps/${param0}/build */
export async function appsBuildBrickapiV1AppsAppBuildPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsBuildBrickapiV1AppsAppBuildPostParams,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  return request<API.AppBuildResp>(`/brickapi/v1/apps/${param0}/build`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Static Serve the frontend static files of the apps. We should move this part to an nginx container instead. GET /brickapi/v1/apps/${param0}/static/${param1} */
export async function appsStaticBrickapiV1AppsAppStaticPathGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsStaticBrickapiV1AppsAppStaticPathGetParams,
  options?: { [key: string]: any },
) {
  const { app: param0, path: param1, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/${param0}/static/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Static Serve the frontend static files of the apps. We should move this part to an nginx container instead. GET /brickapi/v1/apps/${param0}/static/${param1} */
export async function appsStaticBrickapiV1AppsAppStaticPathGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsStaticBrickapiV1AppsAppStaticPathGetParams,
  options?: { [key: string]: any },
) {
  const { app: param0, path: param1, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/${param0}/static/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Submit Data Submit frontend, backend, permission profile and permission model of an app. POST /brickapi/v1/apps/${param0}/submit */
export async function appsSubmitDataBrickapiV1AppsAppSubmitPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsSubmitDataBrickapiV1AppsAppSubmitPostParams,
  body: API.BodyAppsSubmitDataBrickapiV1Apps_app_submitPost,
  frontend_file?: File,
  backend_file?: File,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  const formData = new FormData();

  if (frontend_file) {
    formData.append('frontend_file', frontend_file);
  }

  if (backend_file) {
    formData.append('backend_file', backend_file);
  }

  Object.keys(body).forEach((ele) => {
    const item = (body as any)[ele];

    if (item !== undefined && item !== null) {
      if (typeof item === 'object' && !(item instanceof File)) {
        if (item instanceof Array) {
          item.forEach((f) => formData.append(ele, f || ''));
        } else {
          formData.append(ele, JSON.stringify(item));
        }
      } else {
        formData.append(ele, item);
      }
    }
  });

  return request<API.AppReadWithAllDataResp>(`/brickapi/v1/apps/${param0}/submit`, {
    method: 'POST',
    params: { ...queryParams },
    data: formData,
    requestType: 'form',
    ...(options || {}),
  });
}

/** Apps:Submit Data Submit frontend, backend, permission profile and permission model of an app. POST /brickapi/v1/apps/${param0}/submit */
export async function appsSubmitDataBrickapiV1AppsAppSubmitPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsSubmitDataBrickapiV1AppsAppSubmitPostParams,
  body: API.BodyAppsSubmitDataBrickapiV1Apps_app_submitPost,
  frontend_file?: File,
  backend_file?: File,
  options?: { [key: string]: any },
) {
  const { app: param0, ...queryParams } = params;
  const formData = new FormData();

  if (frontend_file) {
    formData.append('frontend_file', frontend_file);
  }

  if (backend_file) {
    formData.append('backend_file', backend_file);
  }

  Object.keys(body).forEach((ele) => {
    const item = (body as any)[ele];

    if (item !== undefined && item !== null) {
      if (typeof item === 'object' && !(item instanceof File)) {
        if (item instanceof Array) {
          item.forEach((f) => formData.append(ele, f || ''));
        } else {
          formData.append(ele, JSON.stringify(item));
        }
      } else {
        formData.append(ele, item);
      }
    }
  });

  return request<API.AppReadWithAllDataResp>(`/brickapi/v1/apps/${param0}/submit`, {
    method: 'POST',
    params: { ...queryParams },
    data: formData,
    requestType: 'form',
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. GET /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. GET /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. PUT /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions3(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'PUT',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. PUT /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions4(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'PUT',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. POST /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions5(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. POST /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions6(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. DELETE /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions7(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. DELETE /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions8(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. PATCH /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions9(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'PATCH',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Api Call a backend api of an app. PATCH /brickapi/v1/apps/api/${param0} */
export async function appsApiBrickapiV1AppsApiPathOptions10(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.appsApiBrickapiV1AppsApiPathOptionsParams,
  options?: { [key: string]: any },
) {
  const { path: param0, ...queryParams } = params;
  return request<any>(`/brickapi/v1/apps/api/${param0}`, {
    method: 'PATCH',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Apps:Current App GET /brickapi/v1/apps/me */
export async function appsCurrentAppBrickapiV1AppsMeGet(options?: { [key: string]: any }) {
  return request<API.DomainUserAppReadResp>('/brickapi/v1/apps/me', {
    method: 'GET',
    ...(options || {}),
  });
}

/** Apps:Current App GET /brickapi/v1/apps/me */
export async function appsCurrentAppBrickapiV1AppsMeGet2(options?: { [key: string]: any }) {
  return request<API.DomainUserAppReadResp>('/brickapi/v1/apps/me', {
    method: 'GET',
    ...(options || {}),
  });
}
