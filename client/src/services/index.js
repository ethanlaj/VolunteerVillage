// eslint-disable-next-line no-undef
const BASE_URL = process.env.NODE_ENV === 'production'
	? 'https://volunteervillage-api.ethanlaj.dev/'
	: 'http://localhost:8000/';

export default BASE_URL;