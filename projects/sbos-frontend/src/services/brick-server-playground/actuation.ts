// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Post Actuate an entity to a value. Body format {{entity_id: [actuation_value, optional playceholder}, ...} POST /brickapi/v1/actuation/domains/${param0} */
export async function postBrickapiV1ActuationDomainsDomainPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1ActuationDomainsDomainPostParams,
  body: Record<string, any>,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ActuationResultsResp>(`/brickapi/v1/actuation/domains/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Post Actuate an entity to a value. Body format {{entity_id: [actuation_value, optional playceholder}, ...} POST /brickapi/v1/actuation/domains/${param0} */
export async function postBrickapiV1ActuationDomainsDomainPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1ActuationDomainsDomainPostParams,
  body: Record<string, any>,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ActuationResultsResp>(`/brickapi/v1/actuation/domains/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Read Read an entity to a value. POST /brickapi/v1/actuation/domains/${param0}/read */
export async function readBrickapiV1ActuationDomainsDomainReadPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.readBrickapiV1ActuationDomainsDomainReadPostParams,
  body: Record<string, any>,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ActuationResultsResp>(`/brickapi/v1/actuation/domains/${param0}/read`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Read Read an entity to a value. POST /brickapi/v1/actuation/domains/${param0}/read */
export async function readBrickapiV1ActuationDomainsDomainReadPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.readBrickapiV1ActuationDomainsDomainReadPostParams,
  body: Record<string, any>,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.ActuationResultsResp>(`/brickapi/v1/actuation/domains/${param0}/read`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Get Actuation Guards GET /brickapi/v1/actuation/guards */
export async function getActuationGuardsBrickapiV1ActuationGuardsGet(options?: {
  [key: string]: any;
}) {
  return request<API.strListResp>('/brickapi/v1/actuation/guards', {
    method: 'GET',
    ...(options || {}),
  });
}
