export function url(path: string): string {
  const apiRoot =
    typeof window === "undefined"
      ? process.env.API_ROOT
      : process.env.NEXT_PUBLIC_API_ROOT;
  return `${apiRoot}${path}`;
}

export const fetcher = (input: RequestInfo, init?: RequestInit): Promise<any> =>
  fetch(input, init)
    .then((res) => {
      if (res.status !== 200 && res.status !== 201) {
        return undefined;
      }
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      return undefined;
    });

export const fetcherCustom = (
  input: RequestInfo,
  init?: () => any
): Promise<any> =>
  fetcher(input, typeof init === "function" ? init() : undefined);
