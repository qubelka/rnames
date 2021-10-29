import React from 'react'
import { useSelector } from 'react-redux'
import axios from 'axios'

export const Submit = () => {
	const data = useSelector(v => {
		return {
			references: v.ref,
			structured_names: v.sname,
			relations: v.rel,
		}
	})

	const submit = async () => {
		const csrfmiddlewaretoken = document.querySelector(
			'[name=csrfmiddlewaretoken]'
		).value

		axios({
			url: '/tentative_submit_path',
			method: 'POST',
			headers: {
				'X-CSRFToken': csrfmiddlewaretoken,
			},
			data,
		})
			.then(res => console.log(res))
			.catch(err => console.log(err))
	}

	return <button onClick={e => submit()}>Submit</button>
}
