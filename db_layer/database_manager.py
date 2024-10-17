from db_layer.connection import get_connection
from custom_exception.custom_exception import SQLiteException,UpdateException,NoRecordFoundException
class database_manager:
    def __init__(self,logger):
        self.logger=logger
        self.connection=get_connection()

    def create_table(self,table_name,schema):
        query=f"CREATE TABLE IF NOT EXISTS {table_name} {schema}"
        try:
            cursor=self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            # print(f'SQLite error, {e}')
            print("An error occurred.")

    def fetch_data(self,table_name,columns="*",
                   where_clause=None,
                   operator=' AND ',
                   parameters=()):
        columns=(',').join(columns)
        query=f'SELECT {columns} FROM {table_name}'
        if where_clause:
            condition_str=(f'{operator}').join(where_clause)
            query+=f' WHERE {condition_str}'
        try:
            self.logger.log("Data is being fetched from db")
            cursor=self.connection.cursor()
            cursor.execute(query,parameters)
            data=cursor.fetchall()
            self.logger.log(message="Data is fetched successfully.")
            return data
        except Exception as e:
            self.logger.log(message=f"{str(e)}",level="error")
            # print(f"An error occurred.")
            raise SQLiteException()

    def insert_data(self,table_name,columns,values):
        column_str=(',').join(columns)
        placeholder=(',').join(['?']*len(columns))
        query=f'INSERT INTO {table_name} ({column_str}) VALUES ({placeholder}) '
        try:
            cursor=self.connection.cursor()
            # print(query,values)
            cursor.execute(query,values)

            self.connection.commit()
            if cursor.rowcount==1:
                self.logger.log(message="Record inserted successfully.")
                return True
            else:
                # return False
                self.logger.log(message="Record is not inserted",level="error")
                raise SQLiteException()
        except SQLiteException:
            raise
        except Exception as e:
            # print(f'SQLite error, {e}')
            # print("An error occurred.")
            # return False
            self.logger.log(message=str(e),level="error")
            raise SQLiteException()
    def update_data(self,table_name,updates,conditions=None,parameters=[]):
        #updates is dict column_to_be_updated : new value
        columns_to_update=[f'{col}=? ' for col in updates.keys()]
        if columns_to_update:
            columns_to_update=', '.join(columns_to_update)
            query=f'UPDATE {table_name} SET {columns_to_update}'

            if conditions:
                conditions_str=' AND '.join(conditions)
                query+=f' WHERE {conditions_str}'
                # print(query)

            new_values=list(updates.values())

            try:
                cursor=self.connection.cursor()
                print(query)
                print(new_values+parameters)
                cursor.execute(query,new_values+parameters)
                self.connection.commit()
                print(cursor.rowcount)
                if cursor.rowcount == 0:
                    self.logger.log(message="No record is found given id.", level="error")
                    raise NoRecordFoundException()
                else:
                    # print('No record found with given id.')
                    # return False
                   return True

            except NoRecordFoundException as e:
                raise NoRecordFoundException()
            except Exception as e:
                self.logger.log(message=str(e),level="error")

                # print(f'SQLite error, {e}')
                # print('An error has occured.')
                # return False
                raise SQLiteException()
        else:
            self.logger.log(message="No data is provided to update", level="error")
            # # print('-------No data is provided to update-------')
            # return False
            raise UpdateException()

    def delete_data(self,table_name,conditions=None,parameters=[]):
        query=f'DELETE FROM {table_name} '
        condition_str=(' AND ').join(conditions)
        query+=f' WHERE {condition_str} '

        try:
            # print(query)
            cursor=self.connection.cursor()

            cursor.execute(query,parameters)
            self.connection.commit()
            if cursor.rowcount!=0:
                return True
            else:
                # print('No record found with given id.')
                # return False
                raise NoRecordFoundException()

        except NoRecordFoundException:
            raise NoRecordFoundException()
        except Exception as e:
            self.logger.log(message=str(e),level="error")
            # print('An error occured.')
            # # print(f'SQLite error, {e}')
            # return False
            raise SQLiteException()