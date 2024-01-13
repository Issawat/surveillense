export const Fetcher = (baseUrl: string) => ({
  async get<R>(url: string) {
    const res = await fetch(`${baseUrl}/${url}`)
    const data = (await res.json()) as R
    return data
  },
  async post<R>(url: string, body: any) {
    const res = await fetch(`${baseUrl}/${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    const data = (await res.json()) as R
    return data
  }
})
