// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Get Get data of an entity with in a time range. GET /brickapi/v1/data/timeseries/domains/${param0} */
export async function getBrickapiV1DataTimeseriesDomainsDomainGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getBrickapiV1DataTimeseriesDomainsDomainGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.TimeseriesDataResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'GET',
    params: {
      // value_types has a default value: number
      value_types: 'number',

      // limit has a default value: 10
      limit: '10',
      ...queryParams,
    },
    ...(options || {}),
  });
}

/** Get Get data of an entity with in a time range. GET /brickapi/v1/data/timeseries/domains/${param0} */
export async function getBrickapiV1DataTimeseriesDomainsDomainGet2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getBrickapiV1DataTimeseriesDomainsDomainGetParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.TimeseriesDataResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'GET',
    params: {
      // value_types has a default value: number
      value_types: 'number',

      // limit has a default value: 10
      limit: '10',
      ...queryParams,
    },
    ...(options || {}),
  });
}

/** Post Post data. If fields are not given, default values are assumed. POST /brickapi/v1/data/timeseries/domains/${param0} */
export async function postBrickapiV1DataTimeseriesDomainsDomainPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1DataTimeseriesDomainsDomainPostParams,
  body: API.TimeseriesData,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: {
      ...queryParams,
    },
    data: body,
    ...(options || {}),
  });
}

/** Post Post data. If fields are not given, default values are assumed. POST /brickapi/v1/data/timeseries/domains/${param0} */
export async function postBrickapiV1DataTimeseriesDomainsDomainPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1DataTimeseriesDomainsDomainPostParams,
  body: API.TimeseriesData,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    params: {
      ...queryParams,
    },
    data: body,
    ...(options || {}),
  });
}

/** Delete Delete data of an entity with in a time range or all the data if a time range is not given. DELETE /brickapi/v1/data/timeseries/domains/${param0} */
export async function deleteBrickapiV1DataTimeseriesDomainsDomainDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteBrickapiV1DataTimeseriesDomainsDomainDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'DELETE',
    params: {
      ...queryParams,
    },
    ...(options || {}),
  });
}

/** Delete Delete data of an entity with in a time range or all the data if a time range is not given. DELETE /brickapi/v1/data/timeseries/domains/${param0} */
export async function deleteBrickapiV1DataTimeseriesDomainsDomainDelete2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteBrickapiV1DataTimeseriesDomainsDomainDeleteParams,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.EmptyResp>(`/brickapi/v1/data/timeseries/domains/${param0}`, {
    method: 'DELETE',
    params: {
      ...queryParams,
    },
    ...(options || {}),
  });
}
