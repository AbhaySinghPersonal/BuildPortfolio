import Generic as G
import MarketProcessing as MP
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoSuchWindowException
import time
from MarketConfig import LOAD_CHCK_INTVL

def mainMarket():
    driver=None
    while True:
        try:
            print('Test1')
            Cur_Dt_Formatted,Cur_Dt=G.GetCurDate("%Y-%m-%d")
            G.LoadTradeClosedDate()
            IsLoadHis,IsLoadCur=G.IsLoadHistorCur(Cur_Dt_Formatted,Cur_Dt)
            driver=G.getDriver()
            if(IsLoadHis):
                MP.LoadHistory(driver,Cur_Dt_Formatted)
            if(IsLoadCur):
                MP.UpdateCurrent(driver,Cur_Dt)
        except SyntaxError:
            print('Exception SyntaxError')
        except TypeError:
            print('Exception TypeError')
        except NameError:
            print('Exception NameError')
        except IndexError:
            print('Exception IndexError')
        except KeyError:
            print('Exception KeyError')
        except ValueError:
            print('Exception ValueError')
        except AttributeError:
            print('Exception AttributeError')
        except IOError:
            print('Exception IOError')
        except ZeroDivisionError:
            print('Exception ZeroDivisionError')
        except ImportError:
            print('Exception ImportError')
        except NoSuchElementException:
            print('Exception -Did not receice elements')
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
        except NoSuchWindowException:
            print('Exception -Window closed')
        except:
            print('UNCAUGHT EXCEPTION')
        finally:
            if driver:
                print('Going to close Driver')
                try:
                    driver.close()
                    print('after close')
                    driver.quit()
                except:
                    print('Exception in closining driver')
        time.sleep(LOAD_CHCK_INTVL)
mainMarket()
