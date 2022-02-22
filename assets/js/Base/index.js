function SetCookieFunctionality_ShowNotification(Text, Type, Timer = 5000, LevelOfNecessity = 2) {
    document.cookie = `Functionality_N=${ConvertCharPersianToEnglishDecode(Text)}~${Type}~${Timer}~${LevelOfNecessity};path=/`
}

function GetCookieFunctionality_ShowNotification() {
    setTimeout(function () {
        let AllCookies = document.cookie.split(';')
        let Cookie_Key
        let Cookie_Val
        for (let Co of AllCookies) {
            let Key = Co.split('=')[0]
            let Value = Co.split('=')[1]
            if (Key == 'Functionality_N' || Key == ' Functionality_N' || Key == ' Functionality_N ') {
                Cookie_Key = Key
                Cookie_Val = Value
            }
        }
        let Text
        let Type
        let Timer
        let LevelOfNecessity
        try {
            Text = Cookie_Val.split('~')[0] || 'نا مشخص'
            Text = Text.replace('"', '')
            Text = Text.replace("'", '')
            Type = Cookie_Val.split('~')[1] || 'Warning'
            Timer = Cookie_Val.split('~')[2] || 8000
            LevelOfNecessity = Cookie_Val.split('~')[3] || 2
        } catch (e) {
        }
        if (Cookie_Key == 'Functionality_N' || Cookie_Key == ' Functionality_N' || Cookie_Key == ' Functionality_N ') {
            let TextResult = Text
            ShowNotificationMessage(TextResult, Type, Timer, LevelOfNecessity)
        }
        document.cookie = `${Cookie_Key}=Closed; expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`
    })
}

function GetKeyByValue(Obj, Val) {
    return Object.keys(Obj).find(K => Obj[K] === Val);
}


/////////////  Convert English Char & Persian Decode //////////////////////////

function ConvertCharEnglishToPersianDecode(Text) {
    let Dict_Char_Persian_English = {
        'ا': 'a1',
        'آ': 'a2',
        'ب': 'b1',
        'پ': 'p1',
        'ت': 't1',
        'ث': 'c1',
        'ج': 'j1',
        'چ': 'ch',
        'ح': 'h1',
        'خ': 'kh',
        'د': 'd1',
        'ذ': 'z1',
        'ر': 'r1',
        'ز': 'z2',
        'ژ': 'zh',
        'س': 'c2',
        'ش': 'sh',
        'ص': 'c3',
        'ض': 'z3',
        'ط': 't2',
        'ظ': 'z4',
        'ع': 'a3',
        'غ': 'g_',
        'ف': 'f1',
        'ق': 'g5',
        'ک': 'k1',
        'گ': 'k2',
        'ل': 'l1',
        'م': 'm1',
        'ن': 'n1',
        'و': 'v1',
        'ه': 'h2',
        'ی': 'e2',
        ' ': '11',
        '': '22',
    }
    let CharEn = Object.keys(Dict_Char_Persian_English)
    let TextResult = ''
    for (let Index = 0; Index < Text.length; Index++) {
        if (Index % 2 == 0) {
            TextResult += GetKeyByValue(Dict_Char_Persian_English, Text[Index] + Text[Index + 1])
        }
    }
    return TextResult
}


function ConvertCharPersianToEnglishDecode(Text) {
    let Res = ''
    for (let i of Text) {
        try {
            Res += Dict_Char_Persian_English[i]
        } catch (e) {
            Res += i
        }
    }
    return Res
}


function SendAjax(Url, Data = {}, Method = 'POST', Success, Failed) {
    function __Redirect__(response) {
        if (response.__Redirect__ == 'True') {
            setTimeout(function () {
                window.location.href = response.__RedirectURL__
            }, parseInt(response.__RedirectAfter__ || 0))
        }
    }

    function Loading(State) {
        if (State == 'Show') {
            LockAllElements()
            let ContainerLoading = document.createElement('div')
            let CircleLoading = document.createElement('div')
            ContainerLoading.id = 'ContainerLoadingAJAX'
            ContainerLoading.classList.add('ContainerLoadingAJAX')
            ContainerLoading.innerHTML = `
                <div class="LoadingCircle"><span></span></div>
            `
            document.body.appendChild(ContainerLoading)
        } else {
            try {
                UnlockAllElements()
                document.getElementById('ContainerLoadingAJAX').remove()
            } catch (e) {
            }
        }
    }

    if (Success == undefined) {
        Success = function (response) {
            __Redirect__(response)
        }
    }
    if (Failed == undefined) {
        Failed = function (response) {
            ShowNotificationMessage('Could not connect to server ', 'Error', 30000, 2)
        }
    }
    //Loading('Show')
    $.ajax(
        {
            url: Url,
            data: JSON.stringify(Data),
            type: Method,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            },
            success: function (response) {
                __Redirect__(response)
                //Loading('Hide')
                Success(response)
            },
            failed: function (response) {
                __Redirect__(response)
                //Loading('Hide')
                Failed(response)
            },
            error: function (response) {
                __Redirect__(response)
                //Loading('Hide')
                Failed(response)
                RemoveLoading()
            }
        }
    )
}

let LIST_ALL_NOTIFICATIONS_INSTANCE = []
let COUNTER_CREATE_NOTIFICATIONS = 0

class ShowNotificationMessage_Model {
    constructor(Text, Type, Timer = 5000, LevelOfNecessity = 3) {
        COUNTER_CREATE_NOTIFICATIONS += 1
        LIST_ALL_NOTIFICATIONS_INSTANCE.push(this)
        this.ID_Notification = COUNTER_CREATE_NOTIFICATIONS
        this.Index_Notification = LIST_ALL_NOTIFICATIONS_INSTANCE.length - 1

        let ContainerNotifications = document.getElementById('ContainerNotificationsMessage')
        if (ContainerNotifications == undefined) {
            ContainerNotifications = document.createElement('div')
            ContainerNotifications.id = 'ContainerNotificationsMessage'
        }
        let ContainerMessage = document.createElement('div')
        let Message = document.createElement('p')
        let BtnClose = document.createElement('i')
        let Icon = document.createElement('i')

        ContainerMessage.setAttribute('ID_Notification', this.ID_Notification)
        BtnClose.setAttribute('Index_Notification', this.Index_Notification)

        ContainerMessage.classList.add('NotificationMessage')
        ContainerMessage.classList.add(`LevelOfNecessity_${LevelOfNecessity}`)
        ContainerMessage.classList.add(`Notification${Type}`)
        Message.innerText = Text
        BtnClose.className = 'fa fa-times BtnCloseNotification'
        if (Type == 'Success') {
            Icon.className = 'fa fa-check-circle IconNotification IconNotification_Success'
        } else if (Type == 'Error') {
            Icon.className = 'fa fa-times-hexagon IconNotification IconNotification_Error '
        } else if (Type == 'Warning') {
            Icon.className = 'fa fa-exclamation-triangle IconNotification IconNotification_Warning'
        }
        ContainerMessage.appendChild(Icon)
        ContainerMessage.appendChild(BtnClose)
        ContainerMessage.appendChild(Message)
        ContainerNotifications.appendChild(ContainerMessage)
        document.body.appendChild(ContainerNotifications)
        this.ContainerMessage = ContainerMessage
        let Index_Notification = this.Index_Notification
        setTimeout(function () {
            RemoveNotification_Func(Index_Notification)
        }, Timer)

        BtnClose.onclick = function (e) {
            let Index_Notification = e.target.getAttribute('Index_Notification')
            RemoveNotification_Func(Index_Notification)
        }
    }

}

function RemoveNotification_Func(Index) {
    let Instance = LIST_ALL_NOTIFICATIONS_INSTANCE[Index]
    Instance.ContainerMessage.classList.add('Notification_Removed')
    setTimeout(function () {
        Instance.ContainerMessage.remove()
        delete Instance
    }, 300)
}

function ShowNotificationMessage(Text, Type, Timer = 5000, LevelOfNecessity = 3) {
    new ShowNotificationMessage_Model(Text, Type, Timer, LevelOfNecessity)
}


let btnRemoveDetailCart = document.querySelectorAll('[btn-remove-cart-detail]')
for (let btn of btnRemoveDetailCart) {
    btn.addEventListener('click', function () {
        let cartID = this.getAttribute('cartID') || false
        let detailID = this.getAttribute('detailID') || false
        if (cartID && detailID) {
            let productElement = document.querySelector(`[${btn.getAttribute('btn-remove-cart-detail')}]`)
            removeDetailCart(cartID, detailID, productElement)
        }
    })
}

function removeDetailCart(cartID, detailID, productElement) {
    let data = {
        "cartID": String(cartID),
        "detailID": String(detailID)
    }
    SendAjax('/p/removeDetailCart', data, 'POST', function (response) {
        let status = response.status
        if (status == '200') {
            productElement.remove()
            setNewTotalPrice(response.newPrice)
            setNewCountBuy(response.newCount)
        } else {
            ShowNotificationMessage('Cant delete product , product not found')
        }
    })
}

function setNewTotalPrice(price) {
    try {
        document.querySelector('[price-buy-1]').innerText = price
    } catch (e) {
    }
    try {
        document.querySelector('[price-buy-2]').innerText = price
    } catch (e) {
    }
    try {
        document.querySelector('[price-buy-3]').innerText = price
    } catch (e) {
    }
}

function setNewCountBuy(count) {
    try {
        document.querySelector('[count-buy-1]').innerText = count
    } catch (e) {
    }
    try {
        document.querySelector('[count-buy-2]').innerText = count
    } catch (e) {
    }
    try {
        document.querySelector('[count-buy-3]').innerText = count
    } catch (e) {
    }
}

function CreateMessage_Alert(Text, FuncWhenOK, ValueFunc = null, FuncWhenCancel = null) {
    CloseMessage_Alert()
    LockAllElements()
    setTimeout(function () {
        document.body.className = ''

        let Container = document.createElement('div')
        let TextMessage = document.createElement('p')
        let BtnClose = document.createElement('button')
        let BtnOk = document.createElement('button')
        let BtnClose1 = document.createElement('i')


        Container.className = 'ContainerMessage_Alert'
        TextMessage.className = 'TextMessage_Alert'
        BtnClose.className = 'BtnClose_Alert BtnStyle_1'
        BtnOk.className = 'BtnOk_Alert BtnStyle_1'
        BtnClose1.className = 'fa fa-times BtnClose1_Alert'

        TextMessage.innerHTML = Text
        BtnClose.innerText = 'Cancel'
        BtnOk.innerText = 'Yes'

        BtnClose.onclick = function () {
            if (FuncWhenCancel != null) {
                FuncWhenCancel()
            }
            CloseMessage_Alert()
        }
        BtnClose1.onclick = function () {
            if (FuncWhenCancel != null) {
                FuncWhenCancel()
            }
            CloseMessage_Alert()
        }

        BtnOk.onclick = function () {
            if (ValueFunc != null) {
                FuncWhenOK(ValueFunc)
            } else {
                FuncWhenOK()
            }
            CloseMessage_Alert()
        }

        Container.appendChild(TextMessage)
        Container.appendChild(BtnClose)
        Container.appendChild(BtnClose1)
        Container.appendChild(BtnOk)
        ClickOutSideContainer(Container, function () {
            CloseMessage_Alert()
        }, 'OutSide')
        document.body.insertBefore(Container, document.body.firstElementChild)
        BlurAllElementsExceptMessage_Alert()

        // Focus on Button Close
        BtnOk.focus()
    })
}

function CloseMessage_Alert() {
    try {
        document.getElementsByClassName('ContainerMessage_Alert')[0].remove()
    } catch (e) {
    }
    UnlockAllElements()
    Clear_BlurAllElementsExceptMessage_Alert()
}

function BlurAllElementsExceptMessage_Alert() {
    document.body.classList.add('BlurAllElementsExceptMessage_Alert')
    document.body.style.overflow = 'hidden'
}

function Clear_BlurAllElementsExceptMessage_Alert() {
    document.body.classList.remove('BlurAllElementsExceptMessage_Alert')
    document.body.style.overflow = ''
}

function LockAllElements() {
    $('body *').prop('disabled', true)
}

function UnlockAllElements() {
    $('body *').prop('disabled', false)
    $('input[type=checkbox]').prop('disabled', true)
    $('#ContainerForm input[type=radio]').prop('disabled', true)
    $('#ContainerForm input[type=file]').prop('disabled', true)
}

function ClickOutSideContainer(Container, FuncWhenOutSideClick, State = 'Inside') {
    document.addEventListener('click', ClickOutSideCnt = function (event) {
        let IsClickInContainer = Container.contains(event.target);
        if (!IsClickInContainer) {
            if (State == 'OutSide') {
                FuncWhenOutSideClick()
                State = 'Inside'
                document.removeEventListener('click', ClickOutSideCnt)
            }
            State = 'OutSide'
        }
    });
}
