import React from 'react'
import { useDispatch } from 'react-redux'
import { updateRel } from '../store/relations/actions'

export const Relation = ({ relation, formattedName1, formattedName2 }) => {
	const dispatch = useDispatch()

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
				belongs_to: relation.belongs_to == 1 ? 0 : 1
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
				/>
			</td>
			<td>{formattedName2}</td>
		</tr>
	)
}
