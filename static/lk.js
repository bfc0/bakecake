Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            Edit: false,
            Name: userData.name,
            Phone: userData.phone_number,
            Email: userData.email,
            formError: formError || null,
            originalData: {
                name: userData.name,
                phone: userData.phone_number,
                email: userData.email,
            },
            Schema: {
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-я]+$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if (!regex.test(value)) {

                        return '⚠ Недопустимые символы в имени';
                    }
                    return true;
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                }
            }
        }
    },
    methods: {
        ApplyChanges() {
            this.Edit = false
            this.$refs.HiddenFormSubmit.click()
        },
        handleError(error) {
            this.formError = error;
            this.resetForm();
        },
        resetForm() {
            this.Name = this.originalData.name;
            this.Phone = this.originalData.phone;
            this.Email = this.originalData.email;
        },

    },
    mounted() {
        if (this.formError) {
            this.handleError(this.formError);
        }
    }
}).mount('#LK')