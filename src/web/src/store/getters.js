const getters = {
  sidebar: state => state.app.sidebar,
  token: state => state.user.token,
  user_id: state => state.user.user_id,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  roles: state => state.user.roles
}
export default getters
