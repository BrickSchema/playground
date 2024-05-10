// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Post Raw SPARQL for Brick metadata. (May not be exposed in the production deployment. POST /brickapi/v1/domains/${param0}/sparql */
export async function postBrickapiV1DomainsDomainSparqlPost(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1DomainsDomainSparqlPostParams,
  body: string,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.dictResp>(`/brickapi/v1/domains/${param0}/sparql`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/sparql-query',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** Post Raw SPARQL for Brick metadata. (May not be exposed in the production deployment. POST /brickapi/v1/domains/${param0}/sparql */
export async function postBrickapiV1DomainsDomainSparqlPost2(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.postBrickapiV1DomainsDomainSparqlPostParams,
  body: string,
  options?: { [key: string]: any },
) {
  const { domain: param0, ...queryParams } = params;
  return request<API.dictResp>(`/brickapi/v1/domains/${param0}/sparql`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/sparql-query',
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}
