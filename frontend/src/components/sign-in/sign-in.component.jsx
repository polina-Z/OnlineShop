import { Form } from 'antd';
import React, {useState} from 'react';
import {useDispatch} from 'react-redux';
import {useHistory} from 'react-router-dom';
import {setCurrentUserAsync} from '../../redux/user/user.actions';
import { SmartRequest } from '../../utils/utils';
import FormInput from '../form-input/form-input.component';
import CustomButton from '../custom-button/custom-button.component';
import './sign-in.styles.scss';


const LogIn = () => {
    const [form] = Form.useForm();
    const {getFieldError, isFieldTouched, validateFields} = form;
    const dispatch = useDispatch();

    const [isButtonDisabled, setIsButtonDisabled] = useState(true);
    const [isFormErrorHidden, setIsFormErrorHidden] = useState(true);
    const [formError, setFormError] = useState('');
    const [usernameError, setUsernameError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const history = useHistory();

    const onFinish = (values) => {
        SmartRequest.post(
            'login/',
            values,
            {},
            false,
            false
        )
            .then(resp => {
                SmartRequest.setAccessToken(resp.data['access'])
                SmartRequest.get('profile/')
                    .then(resp => {
                        console.log('success in get profile:', resp)
                        const actualUser = resp.data
                        dispatch(setCurrentUserAsync(actualUser))
                        history.push('/')
                    })
            })
            .catch(error => {
                if (error.response && error.response.status === 401) {
                    setFormError(error.response.data['detail'])
                    setIsFormErrorHidden(false)
                } else {
                    console.error('catch on sign in: ', error)
                }
            });
    };


    const onValuesChange = () => {
        setTimeout(() => {
            setIsFormErrorHidden(true);
            setUsernameError(isFieldTouched('username') && Boolean(getFieldError('username').length));
            setPasswordError(isFieldTouched('password') && Boolean(getFieldError('password').length));
            validateFields()
                .then(() => {
                    setIsButtonDisabled(false)
                })
                .catch(() => {
                    setIsButtonDisabled(true)
                })
        }, 0);
    };


    return (
        <div className='sign-in'>
            <h3>I already have an account</h3>
            <span className='title'>Sign in with your username and password</span>
            <Form
                form={form}
                labelCol={{
                    span: 8,
                }}
                wrapperCol={{
                    span: 16,
                }}
                onFinish={onFinish}
                onValuesChange={onValuesChange}
            >
                <Form.Item
                    name='form error'
                    hidden={isFormErrorHidden}
                    wrapperCol={{
                        offset: 8,
                        span: 16,
                    }}
                >
                    <span className="ant-form-item-explain ant-form-item-explain-error">{formError}</span>
                </Form.Item>
                <Form.Item
                    name="username"
                    label="username"
                    validateStatus={usernameError ? 'error' : ''}
                    help={usernameError ? null : ''}
                    rules={[
                        {
                            required: true,
                            message: 'Please input your username!',
                        },
                    ]}
                >
                    <FormInput></FormInput>
                
                </Form.Item>

                <Form.Item
                    name="password"
                    label="password"
                    validateStatus={passwordError ? 'error' : ''}
                    help={passwordError ? null : ''}
                    rules={[
                        {
                            required: true,
                            message: 'Please input your password!',
                        },
                    ]}
                >
                    <FormInput type="password"></FormInput>
                </Form.Item>

                <Form.Item
                    wrapperCol={{
                        offset: 8,
                        span: 16,
                    }}
                >
                    <div className='buttons'>
                        <CustomButton disabled={isButtonDisabled} type="primary" htmlType="submit">SIGN IN</CustomButton>
                    </div>
                </Form.Item>
            </Form>
        </div>
    );
};

export default LogIn;
