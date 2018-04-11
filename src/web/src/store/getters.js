const getters = {
  sidebar: state => state.app.sidebar,
  token: state => state.user.token,
  user_id: state => state.user.user_id,
  avatar: state => state.user.avatar,
  username: state => state.user.username,
  name: state => state.user.name,
  role: state => state.user.role
}
export default getters
