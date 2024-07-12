// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** List Domains GET /brickapi/v1/domains/ */
export async function listDomainsBrickapiV1DomainsGet(options?: { [key: string]: any }) {
  return request<API.DomainReadListResp>('/brickapi/v1/domains/', {
    method: 'GET',
    ...(options || {}),
  });
}

/** List Domains GET /brickapi/v1/domains/ */
export async function listDomainsBrickapiV1DomainsGet2(options?: { [key: string]: any }) {
  return request<API.DomainReadListResp>('/brickapi/v1/domains/', {
    method: 'GET',
    ...(options || {}),
  });
}

/** Get Domain GET /brickapi/v1/domains/${param0} */
export async function getDomainBrickapiV1DomainsDomainGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getDomainBrickapiV1DomainsDomainGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Get Domain GET /brickapi/v1/domains/${param0} */
export async function getDomainBrickapiV1DomainsDomainGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getDomainBrickapiV1DomainsDomainGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Create Domain POST /brickapi/v1/domains/${param0} */
export async function createDomainBrickapiV1DomainsDomainPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createDomainBrickapiV1DomainsDomainPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Create Domain POST /brickapi/v1/domains/${param0} */
export async function createDomainBrickapiV1DomainsDomainPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createDomainBrickapiV1DomainsDomainPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Delete Domain DELETE /brickapi/v1/domains/${param0} */
export async function deleteDomainBrickapiV1DomainsDomainDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainBrickapiV1DomainsDomainDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Delete Domain DELETE /brickapi/v1/domains/${param0} */
export async function deleteDomainBrickapiV1DomainsDomainDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainBrickapiV1DomainsDomainDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain List App GET /brickapi/v1/domains/${param0}/apps */
export async function domainListAppBrickapiV1DomainsDomainAppsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainListAppBrickapiV1DomainsDomainAppsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainAppReadListResp>(`/brickapi/v1/domains/${param0}/apps`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain List App GET /brickapi/v1/domains/${param0}/apps */
export async function domainListAppBrickapiV1DomainsDomainAppsGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainListAppBrickapiV1DomainsDomainAppsGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainAppReadListResp>(`/brickapi/v1/domains/${param0}/apps`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain Get App GET /brickapi/v1/domains/${param0}/apps/${param1} */
export async function domainGetAppBrickapiV1DomainsDomainAppsAppGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainGetAppBrickapiV1DomainsDomainAppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainAppReadResp>(`/brickapi/v1/domains/${param0}/apps/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain Get App GET /brickapi/v1/domains/${param0}/apps/${param1} */
export async function domainGetAppBrickapiV1DomainsDomainAppsAppGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainGetAppBrickapiV1DomainsDomainAppsAppGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainAppReadResp>(`/brickapi/v1/domains/${param0}/apps/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain Approve App POST /brickapi/v1/domains/${param0}/apps/${param1} */
export async function domainApproveAppBrickapiV1DomainsDomainAppsAppPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainApproveAppBrickapiV1DomainsDomainAppsAppPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainAppReadResp>(`/brickapi/v1/domains/${param0}/apps/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Domain Approve App POST /brickapi/v1/domains/${param0}/apps/${param1} */
export async function domainApproveAppBrickapiV1DomainsDomainAppsAppPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.domainApproveAppBrickapiV1DomainsDomainAppsAppPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, app: param1, ...queryParams } = params;
  return request<API.DomainAppReadResp>(`/brickapi/v1/domains/${param0}/apps/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Init Domain GET /brickapi/v1/domains/${param0}/init */
export async function initDomainBrickapiV1DomainsDomainInitGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.initDomainBrickapiV1DomainsDomainInitGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}/init`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Init Domain GET /brickapi/v1/domains/${param0}/init */
export async function initDomainBrickapiV1DomainsDomainInitGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.initDomainBrickapiV1DomainsDomainInitGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}/init`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** List Domain Pre Actuation Policies GET /brickapi/v1/domains/${param0}/policies */
export async function listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadListResp>(
    `/brickapi/v1/domains/${param0}/policies`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** List Domain Pre Actuation Policies GET /brickapi/v1/domains/${param0}/policies */
export async function listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadListResp>(
    `/brickapi/v1/domains/${param0}/policies`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Create Domain Pre Actuation Policy POST /brickapi/v1/domains/${param0}/policies */
export async function createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPostParams,
  body: API.DomainPreActuationPolicyCreate,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadResp>(`/brickapi/v1/domains/${param0}/policies`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Create Domain Pre Actuation Policy POST /brickapi/v1/domains/${param0}/policies */
export async function createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPostParams,
  body: API.DomainPreActuationPolicyCreate,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadResp>(`/brickapi/v1/domains/${param0}/policies`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Delete Domain Pre Actuation Policy DELETE /brickapi/v1/domains/${param0}/policies/${param1} */
export async function deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, policy: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param0}/policies/${param1}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Delete Domain Pre Actuation Policy DELETE /brickapi/v1/domains/${param0}/policies/${param1} */
export async function deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, policy: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param0}/policies/${param1}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Update Domain Pre Actuation Policy PATCH /brickapi/v1/domains/${param0}/policies/${param1} */
export async function updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatch(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatchParams,
  body: API.DomainPreActuationPolicyUpdate,
  options?: { [key: string]: any },
) {
  const { domain: param0, policy: param1, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadResp>(
    `/brickapi/v1/domains/${param0}/policies/${param1}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Update Domain Pre Actuation Policy PATCH /brickapi/v1/domains/${param0}/policies/${param1} */
export async function updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatch2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatchParams,
  body: API.DomainPreActuationPolicyUpdate,
  options?: { [key: string]: any },
) {
  const { domain: param0, policy: param1, ...queryParams } = params;
  return request<API.DomainPreActuationPolicyReadResp>(
    `/brickapi/v1/domains/${param0}/policies/${param1}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** List Resources GET /brickapi/v1/domains/${param0}/resources */
export async function listResourcesBrickapiV1DomainsDomainResourcesGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listResourcesBrickapiV1DomainsDomainResourcesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ResourceConstraintReadListResp>(`/brickapi/v1/domains/${param0}/resources`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** List Resources GET /brickapi/v1/domains/${param0}/resources */
export async function listResourcesBrickapiV1DomainsDomainResourcesGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listResourcesBrickapiV1DomainsDomainResourcesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ResourceConstraintReadListResp>(`/brickapi/v1/domains/${param0}/resources`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Uplaod a Turtle file Upload a Turtle file. An example file: https://gitlab.com/jbkoh/brick-server-dev/blob/dev/examples/data/bldg.ttl POST /brickapi/v1/domains/${param0}/upload */
export async function uploadTurtleFileBrickapiV1DomainsDomainUploadPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.uploadTurtleFileBrickapiV1DomainsDomainUploadPostParams,
  body: API.BodyUploadTurtleFileBrickapiV1Domains_domain_uploadPost,
  file?: File,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  const formData = new FormData();

  if (file) {
    formData.append('file', file);
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

  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}/upload`, {
    method: 'POST',
    params: { ...queryParams },
    data: formData,
    requestType: 'form',
    ...(options || {}),
  });
}

/** Uplaod a Turtle file Upload a Turtle file. An example file: https://gitlab.com/jbkoh/brick-server-dev/blob/dev/examples/data/bldg.ttl POST /brickapi/v1/domains/${param0}/upload */
export async function uploadTurtleFileBrickapiV1DomainsDomainUploadPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.uploadTurtleFileBrickapiV1DomainsDomainUploadPostParams,
  body: API.BodyUploadTurtleFileBrickapiV1Domains_domain_uploadPost,
  file?: File,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  const formData = new FormData();

  if (file) {
    formData.append('file', file);
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

  return request<API.DomainReadResp>(`/brickapi/v1/domains/${param0}/upload`, {
    method: 'POST',
    params: { ...queryParams },
    data: formData,
    requestType: 'form',
    ...(options || {}),
  });
}

/** List Domain User GET /brickapi/v1/domains/${param0}/users */
export async function listDomainUserBrickapiV1DomainsDomainUsersGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainUserBrickapiV1DomainsDomainUsersGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserReadListResp>(`/brickapi/v1/domains/${param0}/users`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** List Domain User GET /brickapi/v1/domains/${param0}/users */
export async function listDomainUserBrickapiV1DomainsDomainUsersGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainUserBrickapiV1DomainsDomainUsersGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.DomainUserReadListResp>(`/brickapi/v1/domains/${param0}/users`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Get Domain User GET /brickapi/v1/domains/${param0}/users/${param1} */
export async function getDomainUserBrickapiV1DomainsDomainUsersUserGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getDomainUserBrickapiV1DomainsDomainUsersUserGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserReadResp>(`/brickapi/v1/domains/${param0}/users/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Get Domain User GET /brickapi/v1/domains/${param0}/users/${param1} */
export async function getDomainUserBrickapiV1DomainsDomainUsersUserGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getDomainUserBrickapiV1DomainsDomainUsersUserGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserReadResp>(`/brickapi/v1/domains/${param0}/users/${param1}`, {
    method: 'GET',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Add Domain User POST /brickapi/v1/domains/${param0}/users/${param1} */
export async function addDomainUserBrickapiV1DomainsDomainUsersUserPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.addDomainUserBrickapiV1DomainsDomainUsersUserPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserReadResp>(`/brickapi/v1/domains/${param0}/users/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Add Domain User POST /brickapi/v1/domains/${param0}/users/${param1} */
export async function addDomainUserBrickapiV1DomainsDomainUsersUserPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.addDomainUserBrickapiV1DomainsDomainUsersUserPostParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserReadResp>(`/brickapi/v1/domains/${param0}/users/${param1}`, {
    method: 'POST',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** List Domain User Profile GET /brickapi/v1/domains/${param0}/users/${param1}/profiles */
export async function listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserProfileReadListResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** List Domain User Profile GET /brickapi/v1/domains/${param0}/users/${param1}/profiles */
export async function listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserProfileReadListResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles`,
    {
      method: 'GET',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Add Domain User Profile POST /brickapi/v1/domains/${param0}/users/${param1}/profiles */
export async function addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPostParams,
  body: API.DomainUserProfileCreate,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserProfileReadResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Add Domain User Profile POST /brickapi/v1/domains/${param0}/users/${param1}/profiles */
export async function addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPostParams,
  body: API.DomainUserProfileCreate,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, ...queryParams } = params;
  return request<API.DomainUserProfileReadResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Delete Domain User Profile DELETE /brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2} */
export async function deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, profile: param2, ...queryParams } = params;
  return request<API.EmptyResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2}`,
    {
      method: 'DELETE',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Delete Domain User Profile DELETE /brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2} */
export async function deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, profile: param2, ...queryParams } = params;
  return request<API.EmptyResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2}`,
    {
      method: 'DELETE',
      params: { ...queryParams },
      ...(options || {}),
    },
  );
}

/** Update Domain User Profile PATCH /brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2} */
export async function updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatch(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatchParams,
  body: API.DomainUserProfileUpdate,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, profile: param2, ...queryParams } = params;
  return request<API.DomainUserProfileReadResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Update Domain User Profile PATCH /brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2} */
export async function updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatch2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatchParams,
  body: API.DomainUserProfileUpdate,
  options?: { [key: string]: any },
) {
  const { domain: param0, user: param1, profile: param2, ...queryParams } = params;
  return request<API.DomainUserProfileReadResp>(
    `/brickapi/v1/domains/${param0}/users/${param1}/profiles/${param2}`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Update Resource POST /brickapi/v1/domains/${param1}/resources/${param0} */
export async function updateResourceBrickapiV1DomainsDomainResourcesEntityIdPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateResourceBrickapiV1DomainsDomainResourcesEntityIdPostParams,
  body: API.ResourceConstraintUpdate,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.ResourceConstraintReadResp>(
    `/brickapi/v1/domains/${param1}/resources/${param0}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Update Resource POST /brickapi/v1/domains/${param1}/resources/${param0} */
export async function updateResourceBrickapiV1DomainsDomainResourcesEntityIdPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateResourceBrickapiV1DomainsDomainResourcesEntityIdPostParams,
  body: API.ResourceConstraintUpdate,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.ResourceConstraintReadResp>(
    `/brickapi/v1/domains/${param1}/resources/${param0}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      params: { ...queryParams },
      data: body,
      ...(options || {}),
    },
  );
}

/** Delete Resource DELETE /brickapi/v1/domains/${param1}/resources/${param0} */
export async function deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDeleteParams,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param1}/resources/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Delete Resource DELETE /brickapi/v1/domains/${param1}/resources/${param0} */
export async function deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDeleteParams,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param1}/resources/${param0}`, {
    method: 'DELETE',
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** Notify Resource POST /brickapi/v1/domains/${param1}/resources/${param0}/notify */
export async function notifyResourceBrickapiV1DomainsDomainResourcesEntityIdNotifyPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.notifyResourceBrickapiV1DomainsDomainResourcesEntityIdNotifyPostParams,
  body: API.ResourceConstraintUpdate,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param1}/resources/${param0}/notify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Notify Resource POST /brickapi/v1/domains/${param1}/resources/${param0}/notify */
export async function notifyResourceBrickapiV1DomainsDomainResourcesEntityIdNotifyPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.notifyResourceBrickapiV1DomainsDomainResourcesEntityIdNotifyPostParams,
  body: API.ResourceConstraintUpdate,
  options?: { [key: string]: any },
) {
  const { entity_id: param0, domain: param1, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/domains/${param1}/resources/${param0}/notify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}
