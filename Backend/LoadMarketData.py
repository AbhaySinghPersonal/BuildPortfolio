import Generic as G
import MarketProcessing as MP
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoSuchWindowException
import time
from MarketConfig import LOAD_CHCK_INTVL,LIST_OF_ALL
from pathlib import Path
import GenericDB as GDB

def mainMarket():
    driver=None
    while True:
        try:
            Cur_Dt_Formatted,Cur_Dt,IsWeekEnd=G.GetCurDate("%Y-%m-%d")
            G.LoadTradeClosedDate()
            my_file = Path(LIST_OF_ALL)
            if my_file.is_file():
                MP.LoadHistory(Cur_Dt_Formatted)
                G.RemoveFile(LIST_OF_ALL)
                print("Sleeping for "+str(LOAD_CHCK_INTVL)+" seconds")
                time.sleep(LOAD_CHCK_INTVL)
            else:
                print('No Stock History to Load: Not Exist'+LIST_OF_ALL)
            
            if not IsWeekEnd:
                SegOnHldy=GDB.IsGivenDtHoliday(Cur_Dt_Formatted)
                MP.UpdateCurrent(Cur_Dt,Cur_Dt_Formatted,SegOnHldy)
            print("Sleeping for "+str(LOAD_CHCK_INTVL)+" seconds")
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
        time.sleep(LOAD_CHCK_INTVL)
mainMarket()
