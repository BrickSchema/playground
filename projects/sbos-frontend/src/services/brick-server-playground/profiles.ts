// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** List Profiles GET /brickapi/v1/profiles/ */
export async function listProfilesBrickapiV1ProfilesGet(options?: { [key: string]: any }) {
  return request<API.PermissionProfileReadListResp>('/brickapi/v1/profiles/', {
    method: 'GET',
    ...(options || {}),
  });
}

/** List Profiles GET /brickapi/v1/profiles/ */
export async function listProfilesBrickapiV1ProfilesGet2(options?: { [key: string]: any }) {
  return request<API.PermissionProfileReadListResp>('/brickapi/v1/profiles/', {
    method: 'GET',
    ...(options || {}),
  });
}

/** Create Profile POST /brickapi/v1/profiles/ */
export async function createProfileBrickapiV1ProfilesPost(
  body: API.PermissionProfileCreate,
  options?: { [key: string]: any },
) {
  return request<API.PermissionProfileReadResp>('/brickapi/v1/profiles/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Create Profile POST /brickapi/v1/profiles/ */
export async function createProfileBrickapiV1ProfilesPost2(
  body: API.PermissionProfileCreate,
  options?: { [key: string]: any },
) {
  return request<API.PermissionProfileReadResp>('/brickapi/v1/profiles/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Get Profile GET /brickapi/v1/profiles/${param0} */
export async function getProfileBrickapiV1ProfilesProfileGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getProfileBrickapiV1ProfilesProfileGetParams,
  options?: { [key: string]: any },
) {
  const { profile: param0, ...queryParams } = params;
  return request<API.PermissionProfileReadResp>(`/brickapi/v1/profiles/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Get Profile GET /brickapi/v1/profiles/${param0} */
export async function getProfileBrickapiV1ProfilesProfileGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getProfileBrickapiV1ProfilesProfileGetParams,
  options?: { [key: string]: any },
) {
  const { profile: param0, ...queryParams } = params;
  return request<API.PermissionProfileReadResp>(`/brickapi/v1/profiles/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Update Profile POST /brickapi/v1/profiles/${param0} */
export async function updateProfileBrickapiV1ProfilesProfilePost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateProfileBrickapiV1ProfilesProfilePostParams,
  body: API.PermissionProfileUpdate,
  options?: { [key: string]: any },
) {
  const { profile: param0, ...queryParams } = params;
  return request<API.PermissionProfileReadResp>(`/brickapi/v1/profiles/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Update Profile POST /brickapi/v1/profiles/${param0} */
export async function updateProfileBrickapiV1ProfilesProfilePost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateProfileBrickapiV1ProfilesProfilePostParams,
  body: API.PermissionProfileUpdate,
  options?: { [key: string]: any },
) {
  const { profile: param0, ...queryParams } = params;
  return request<API.PermissionProfileReadResp>(`/brickapi/v1/profiles/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}
