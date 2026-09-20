const TOKEN_KEY = "calbell_token";

const Api = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },
  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  },
  isLoggedIn() {
    return !!this.getToken();
  },

  async _request(path, options = {}) {
    const headers = options.headers || {};
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(path, { ...options, headers });

    if (response.status === 401) {
      this.clearToken();
      window.dispatchEvent(new CustomEvent("calbell:unauthorized"));
    }

    if (!response.ok) {
      let detail = `Request failed (${response.status})`;
      try {
        const body = await response.json();
        detail = body.detail || detail;
      } catch (e) {
        /* ignore */
      }
      throw new Error(detail);
    }

    if (response.status === 204) return null;
    return response.json();
  },

  async register(email, password) {
    const data = await this._request("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.access_token);
    return data;
  },

  async login(email, password) {
    const body = new URLSearchParams();
    body.set("username", email);
    body.set("password", password);
    const data = await this._request("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    this.setToken(data.access_token);
    return data;
  },

  logout() {
    this.clearToken();
  },

  me() {
    return this._request("/api/me");
  },

  updateGoals(goals) {
    return this._request("/api/me/goals", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(goals),
    });
  },

  getDiary(dateStr) {
    return this._request(`/api/diary?for_date=${dateStr}`);
  },

  addEntry(entry) {
    return this._request("/api/diary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    });
  },

  deleteEntry(id) {
    return this._request(`/api/diary/${id}`, { method: "DELETE" });
  },

  lookupBarcode(code) {
    return this._request(`/api/barcode/${encodeURIComponent(code)}`);
  },

  async recognizePhoto(blob) {
    const formData = new FormData();
    formData.append("file", blob, "photo.jpg");
    return this._request("/api/recognize", {
      method: "POST",
      body: formData,
    });
  },
};
