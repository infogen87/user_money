from fastapi import APIRouter, Depends, HTTPException

from schemas.account import AccountCreatePayload
from schemas.transaction import DepositTransactionPayload, WithdrawalTransactinPayload
from services.account import account_service
from deps import get_current_user


account_router = APIRouter()


@account_router.post("")
def create_account(
    account_data: AccountCreatePayload,
    current_user=Depends(get_current_user)
):
    new_account = account_service.create_account(account_data, current_user)
    return new_account


@account_router.get("")
def get_account(current_user=Depends(get_current_user)):
    account = account_service.get_account(current_user)
    return account


@account_router.post("/deposit")
def transact(transaction: DepositTransactionPayload, current_user=Depends(get_current_user), account=Depends(get_account)):

    return account_service.deposit_money(transaction, account.id)


@account_router.post("/withdraw")
def transact(transaction: WithdrawalTransactinPayload, current_user=Depends(get_current_user), account=Depends(get_account)):
    if transaction.amount > account.balance:
        raise HTTPException(status_code=422, detail="insufficient fund")
    if transaction.amount <= 5:
        raise HTTPException(status_code=422, detail="withdrawal amount is too low") 

    new_balance = account_service.withdraw_money(transaction, account.id)
    return {"message": "withdrawal successful", "new balance": f"{new_balance}"}
