import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { formatStructuredName } from '../utilities'
import { updateRel } from '../store/relations/actions'

export const Relation = ({ relation }) => {
	const dispatch = useDispatch()
	const [formattedName1, formattedName2] = useSelector(state => {
		return [
			formatStructuredName(state.map[relation.name1], state),
			formatStructuredName(state.map[relation.name2], state),
		]
	})

	const swap = () => {
		dispatch(
			updateRel({
				...relation,
				name1: relation.name2,
				name2: relation.name1,
			})
		)
	}

	const belongs = () => {
		dispatch(
			updateRel({
				...relation,
				belongs_to: relation.belongs_to == 1 ? 0 : 1,
			})
		)
	}

	return (
		<tr>
			<td>{formattedName1}</td>
			<td>
				<button className='w3-btn' onClick={swap}>
					↔
				</button>
			</td>
			<td>
				<input
					className='w3-check'
					type='checkbox'
					onChange={belongs}
					checked={relation.belongs_to}
				/>
			</td>
			<td>{formattedName2}</td>
		</tr>
	)
}
