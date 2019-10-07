from app import db
from models import Money, MoneyTotal
from sqlalchemy import desc

def addmoney(currency, value, total):
    countmoney = Money.query.filter(Money.value == value).filter(Money.currency == currency).count()
    
    if countmoney == 0:
        new = Money(currency=currency, value=value, total=total)
        db.session.add(new)
    else:
        finded = Money.query.filter(Money.value == value).filter(Money.currency == currency).first()
        finded.total = finded.total + total
    
    deposit = value * total
    
    if MoneyTotal.query.filter(Money.currency == currency).count() == 0:
        newtotal = MoneyTotal(currency=currency, total=deposit)
        db.session.add(newtotal)
    else:
        findedtotal = MoneyTotal.query.filter(MoneyTotal.currency == currency).first()
        findedtotal.total = MoneyTotal.total + deposit
    try:
        db.session.commit()
    except:
        db.session.rollback()
    else:
        return True
    finally:
        db.session.close()
    return False

def getmoney(currency, amount):
    msge = {'success': False, 'errormsg': 'Невозможно выполнить операцию - нет в наличии!'}
    msgs = {'success': True}
    if MoneyTotal.query.filter(MoneyTotal.currency == currency).count() == 0:
        return msge
    
    findedtotal = MoneyTotal.query.filter(MoneyTotal.currency == currency).first()
    if findedtotal.total < amount:
        return msge
    
    r = False
    ms = Money.query.filter(Money.currency==currency).order_by(desc(Money.value)).all()
    resultlist = []
    for m in ms:
        
        #Если количество больше номинала 
        if amount >= m.value and m.total != 0:
            #print(amount)
            #print('номинал ' + str(m.value))
            o = amount%m.value
            #Если нет остатка от деления
            #print(o)
            if o == 0:
                #print('if0')
                t = int(amount/m.value)
                #print(t)
                #print(m.total)
                mt = m.total
                m.total = m.total - t
                findedtotal.total = findedtotal.total - amount
                #Если есть количество банкнот больше или равно
                resultlist.append({'value': m.value, 'quantity': t})
                #print(mt)
                #print(t)
                if mt >= t:
                    r=True
                    break
                    #Ставим результат успешным, завершаем цикл
                else:
                    amount = amount - int(t*m.value)
            else:
                #делящеейся количество
                amount = amount - o
                t = amount/m.value
                m.total = m.total - t
                findedtotal.total = findedtotal.total - amount
                amount = amount - int(t*m.value)+o
                resultlist.append({'value': m.value, 'quantity': t})
                #print('amount ' + str(amount))
                #в следущем цикле попробуем ещё раз номиналом ниже
        
    if r:
        try:
            db.session.commit()
        except:
            db.session.rollback()
        else:
            msgs['result'] = resultlist
            return msgs
        finally:
            db.session.close()
    
    return msge
        
    
    
    