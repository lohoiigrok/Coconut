from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from project.db_models.models import AccountTransactionTemplate
import pytest

def test_accounts_transaction_template(db_session: Session):
    stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_name()}", balance=1000)
    bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_name()}", balance=500)

    db_session.add_all([stan, bob])
    db_session.commit()

    def transfer_money(session, from_account, to_account, amount):
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        from_account.balance -= amount
        to_account.balance += amount

        session.commit()

    assert stan.balance == 1000
    assert bob.balance == 500

    try:
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

        assert stan.balance == 800
        assert bob.balance == 700

    except Exception as e:
        db_session.rollback()
        pytest.fail(f"Ошибка при переводе денег: {e}")

    finally:
        db_session.delete(stan)
        db_session.delete(bob)
        db_session.commit()
