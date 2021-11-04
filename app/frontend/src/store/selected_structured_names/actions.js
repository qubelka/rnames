import { SELECT_STRUCTURED_NAME } from '../action-types.js'

export const selectStructuredName = structured_name_id => {
	return {
		type: SELECT_STRUCTURED_NAME,
		structured_name_id,
	}
}
