import React from 'react'
import { useDispatch } from 'react-redux'
import { addName } from '../store/map/actions'
import { NameEntry } from './NameEntry'
import { makeId } from '../utilities'

export const NameList = ({ data }) => {
	const dispatch = useDispatch()
	const addNew = e => {
		const name = {
			id: makeId('name'),
			name: '',
			variant: 'name',
			qualifier: 'bio',
			level: 1,
		}
		dispatch(addName(data.id, name))
	}

	return (
		<div>
			{data.names.map(v => (
				<NameEntry {...{ key: v.id, id: v.id, data }} />
			))}
			<button type='button' onClick={addNew}>
				Add new name
			</button>
		</div>
	)
}
