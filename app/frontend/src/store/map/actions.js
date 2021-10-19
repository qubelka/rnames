import {
	MAP_VALUE,
	INITIALIZE_MAP_VALUES,
	ADD_NAME,
	UPDATE_NAME,
} from '../action-types'

export const mapId = (key, value) => (dispatch, getState) => {
	dispatch({
		type: MAP_VALUE,
		key,
		value,
	})
}

export const initMapvalues = map => (dispatch, getState) => {
	dispatch({
		type: INITIALIZE_MAP_VALUES,
		map,
	})
}

export const addName = (refId, name) => (dispatch, getState) => {
	dispatch({
		type: ADD_NAME,
		refId,
		name,
	})
}

export const updateName = (refId, name, nameId) => (dispatch, getState) => {
	dispatch({
		type: UPDATE_NAME,
		refId,
		name,
		nameId,
	})
}
